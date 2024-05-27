# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the pid endpoints."""

import json
from unittest.mock import patch

from flask import url_for

from project import base_url
from project.api.models import Configuration, Contact, Device, Platform, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl, pidinst
from project.tests.base import BaseTestCase


class SetupMixin:
    """Mixin to provide easier access to example data."""

    def setup_normal_user(self):
        """Set a normal user up, so that we can work with it."""
        contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(subject=contact.email, contact=contact)
        db.session.add_all([contact, self.normal_user])
        db.session.commit()

    def setup_super_user(self):
        """Set a super user up, so that we can work with it."""
        contact = Contact(
            given_name="super", family_name="contact", email="super.contact@localhost"
        )
        self.super_user = User(
            subject=contact.email, contact=contact, is_superuser=True
        )
        db.session.add_all([contact, self.super_user])
        db.session.commit()

    def setup_public_device_in_group_123(self):
        """Set a public device up."""
        self.public_device = Device(
            short_name="public_device_in_group_123",
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=["123"],
        )
        db.session.add(self.public_device)
        db.session.commit()

    def setup_public_platform_in_group_123(self):
        """Set a public platform up."""
        self.public_platform = Platform(
            short_name="public_platform_in_group_123",
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=["123"],
        )
        db.session.add(self.public_platform)
        db.session.commit()

    def setup_public_configuration_in_group_123(self):
        """Set a public configuration up."""
        self.public_configuration = Configuration(
            label="public_configuration_in_group_123",
            is_public=True,
            is_internal=False,
            cfg_permission_group="123",
        )
        db.session.add(self.public_configuration)
        db.session.commit()


class TestPids(BaseTestCase, SetupMixin):
    """Some tests for the pid endpoints."""

    pid_url = f"{base_url}/pids"

    def test_get_list(self):
        """Ensure the get list is not allowed."""
        resp = self.client.get(self.pid_url)
        self.assertEqual(resp.status_code, 405)

    def test_get_one(self):
        """Ensure we can't use the get detail endpoint."""
        resp = self.client.get(f"{self.pid_url}/1")
        self.assertEqual(resp.status_code, 405)

    def test_patch(self):
        """Ensure we can't use the patch endpoint."""
        resp = self.client.patch(
            f"{self.pid_url}/1", content_type="application/vnd.api+json"
        )
        self.assertEqual(resp.status_code, 405)

    def test_delete(self):
        """Ensure we can't use the delete endpoint."""
        resp = self.client.delete(f"{self.pid_url}/1")
        self.assertEqual(resp.status_code, 405)

    def test_post_without_user(self):
        """Ensure we need an user to post."""
        resp = self.client.post(self.pid_url, content_type="application/vnd.api+json")
        self.assertEqual(resp.status_code, 401)

    def test_post_no_payload(self):
        """Ensure we require some input data."""
        self.setup_normal_user()
        with self.run_requests_as(self.normal_user):
            resp = self.client.post(
                self.pid_url,
                data=json.dumps(dict()),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 400)

    def test_post_missing_type_and_id_payload(self):
        """Ensure we require some input data."""
        self.setup_normal_user()
        payload = {"instrument_instance": {}}
        with self.run_requests_as(self.normal_user):
            resp = self.client.post(
                self.pid_url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 400)

    def test_post_unsupported_type_payload(self):
        """Ensure we require some input data."""
        self.setup_normal_user()
        payload = {
            "instrument_instance": {
                "type": "user",
                "id": self.normal_user.id,
            }
        }
        with self.run_requests_as(self.normal_user):
            resp = self.client.post(
                self.pid_url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 400)

    def test_post_entity_not_found(self):
        """Ensure we return 404 if the entity was not found."""
        self.setup_normal_user()
        payload = {"instrument_instance": {"type": "device", "id": "1234567890"}}
        with self.run_requests_as(self.normal_user):
            resp = self.client.post(
                self.pid_url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 404)

    def test_post_not_editable(self):
        """Ensure we check the permissions to edit the entities."""
        self.setup_normal_user()
        self.setup_public_device_in_group_123()
        payload = {
            "instrument_instance": {"type": "device", "id": self.public_device.id}
        }
        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=1,
                    username="mock",
                    administrated_permission_groups=[],
                    membered_permission_groups=[],
                )
                resp = self.client.post(
                    self.pid_url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(resp.status_code, 403)

    def test_post_existing_pid(self):
        """Ensure we can't add pids for devices that have already one."""
        self.setup_super_user()
        self.setup_public_device_in_group_123()
        self.public_device.persistent_identifier = "42/1234567890"
        db.session.add(self.public_device)
        db.session.commit()

        payload = {
            "instrument_instance": {"type": "device", "id": self.public_device.id}
        }
        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.pid_url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 409)

    def test_post_pid_for_device(self):
        """Ensure we get a pid for a devices."""
        self.setup_super_user()
        self.setup_public_device_in_group_123()

        payload = {
            "instrument_instance": {"type": "device", "id": self.public_device.id}
        }
        persistent_identifier = "42/1234567890"
        with self.run_requests_as(self.super_user):
            with patch.object(pidinst, "create_pid") as mock:
                mock.return_value = persistent_identifier
                resp = self.client.post(
                    self.pid_url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(resp.status_code, 200)
        reloaded_device = (
            db.session.query(Device).filter_by(id=self.public_device.id).first()
        )

        self.assertEqual(reloaded_device.persistent_identifier, persistent_identifier)
        self.assertEqual(
            reloaded_device.update_description, "create;persistent identifier"
        )
        self.assertEqual(reloaded_device.updated_by, self.super_user)

    def test_post_pid_for_private_device(self):
        """Ensure we don't get a pid for a private devices."""
        self.setup_super_user()
        self.setup_public_device_in_group_123()
        private_device = self.public_device

        private_device.is_public = False
        private_device.is_private = True
        private_device.create_by = self.super_user.contact

        db.session.add(private_device)
        db.session.commit()

        payload = {"instrument_instance": {"type": "device", "id": private_device.id}}
        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.pid_url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 409)

    def test_post_pid_for_platform(self):
        """Ensure we get a pid for a platforms."""
        self.setup_super_user()
        self.setup_public_platform_in_group_123()

        payload = {
            "instrument_instance": {"type": "platform", "id": self.public_platform.id}
        }
        persistent_identifier = "42/1234567890"
        with self.run_requests_as(self.super_user):
            with patch.object(pidinst, "create_pid") as mock:
                mock.return_value = persistent_identifier
                resp = self.client.post(
                    self.pid_url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(resp.status_code, 200)
        reloaded_platform = (
            db.session.query(Platform).filter_by(id=self.public_platform.id).first()
        )

        self.assertEqual(reloaded_platform.persistent_identifier, persistent_identifier)
        self.assertEqual(
            reloaded_platform.update_description, "create;persistent identifier"
        )
        self.assertEqual(reloaded_platform.updated_by, self.super_user)

    def test_post_pid_for_private_platform(self):
        """Ensure we don't get a pid for a private platforms."""
        self.setup_super_user()
        self.setup_public_platform_in_group_123()
        private_platform = self.public_platform

        private_platform.is_public = False
        private_platform.is_private = True
        private_platform.create_by = self.super_user.contact

        db.session.add(private_platform)
        db.session.commit()

        payload = {
            "instrument_instance": {"type": "platform", "id": private_platform.id}
        }
        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.pid_url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 409)

    def test_post_pid_for_configuration(self):
        """Ensure we get a pid for a configurations."""
        self.setup_super_user()
        self.setup_public_configuration_in_group_123()

        payload = {
            "instrument_instance": {
                "type": "configuration",
                "id": self.public_configuration.id,
            }
        }
        persistent_identifier = "42/1234567890"
        with self.run_requests_as(self.super_user):
            with patch.object(pidinst, "create_pid") as mock:
                mock.return_value = persistent_identifier
                resp = self.client.post(
                    self.pid_url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(resp.status_code, 200)
        reloaded_configuration = (
            db.session.query(Configuration)
            .filter_by(id=self.public_configuration.id)
            .first()
        )

        self.assertEqual(
            reloaded_configuration.persistent_identifier, persistent_identifier
        )
        self.assertEqual(
            reloaded_configuration.update_description, "create;persistent identifier"
        )
        self.assertEqual(reloaded_configuration.updated_by, self.super_user)

    def test_openapi(self):
        """Ensure the openapi contains the pid endpoint."""
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        self.assertEqual(response.status_code, 200)

        openapi_specs = response.json
        paths = openapi_specs["paths"]

        endpoint_url = self.pid_url.replace(base_url, "")
        self.assertIn(endpoint_url, paths.keys())

        path_endpoint = paths[endpoint_url]
        self.assertIn("post", path_endpoint.keys())
