# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the restoring configurations."""

import json

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    PermissionGroup,
    PermissionGroupMembership,
    Site,
    User,
)
from project.api.models.base_model import db
from project.extensions.instances import mqtt
from project.tests.base import BaseTestCase


class TestRestoreConfigurations(BaseTestCase):
    """Test class to restore configurations."""

    configurations_url = base_url + "/configurations"

    def setUp(self):
        """Set up some data to test with."""
        super().setUp()

        contact1 = Contact(
            given_name="test", family_name="user", email="test.user@localhost"
        )
        contact2 = Contact(
            given_name="super", family_name="user", email="super.user@localhost"
        )
        self.normal_user = User(subject=contact1.email, contact=contact1)
        self.super_user = User(
            subject=contact2.email, contact=contact2, is_superuser=True
        )
        self.configuration = Configuration(
            label="archived configuration",
            is_public=True,
            is_internal=False,
            archived=True,
            update_description="create;basic data",
        )
        self.permission_group = PermissionGroup(name="test", entitlement="test")
        self.other_group = PermissionGroup(name="other", entitlement="other")
        self.membership = PermissionGroupMembership(
            permission_group=self.permission_group, user=self.normal_user
        )
        db.session.add_all(
            [
                contact1,
                contact2,
                self.normal_user,
                self.super_user,
                self.configuration,
                self.permission_group,
                self.other_group,
                self.membership,
            ]
        )
        db.session.commit()

    def test_get(self):
        """Ensure that it is not allowed to use the get method."""
        response = self.client.get(f"{self.configurations_url}/12345/restore")
        self.assertEqual(response.status_code, 405)

    def test_post_unauthorized(self):
        """Ensure that we don't allow anonymous to restore."""
        response = self.client.post(f"{self.configurations_url}/12345/restore")
        self.assertEqual(response.status_code, 401)

    def test_post_nonexisting(self):
        """Ensure that we got an 404 when the configuration doesn't exist."""
        with self.run_requests_as(self.normal_user):
            response = self.client.post(f"{self.configurations_url}/12345/restore")
        self.assertEqual(response.status_code, 404)

    def test_post_user_not_in_any_group(self):
        """Ensure that an ordinary user without group membership can't restore."""
        self.configuration.cfg_permission_group = str(self.other_group.id)
        db.session.add(self.configuration)
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.configuration.id}/restore"
            )
        self.assertEqual(response.status_code, 403)

    def test_post_member_in_a_group(self):
        """Ensure that we can unset the archived flag as members."""
        self.configuration.cfg_permission_group = str(self.permission_group.id)
        db.session.add(self.configuration)
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.configuration.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_configuration = (
            db.session.query(Configuration).filter_by(id=self.configuration.id).one()
        )
        self.assertFalse(reloaded_configuration.archived)
        self.assertEqual(
            reloaded_configuration.update_description, "restore;basic data"
        )
        self.assertEqual(reloaded_configuration.updated_by_id, self.normal_user.id)
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called_once()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/patch-configuration")
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal("configuration")
        self.expect(notification_data["attributes"]["archived"]).to_equal(False)
        self.expect(notification_data["attributes"]["label"]).to_equal(
            self.configuration.label
        )

    def test_post_superuser(self):
        """Ensure that we can unset the archived flag super user."""
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.configuration.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_configuration = (
            db.session.query(Configuration).filter_by(id=self.configuration.id).one()
        )
        self.assertFalse(reloaded_configuration.archived)
        self.assertEqual(
            reloaded_configuration.update_description, "restore;basic data"
        )
        self.assertEqual(reloaded_configuration.updated_by_id, self.super_user.id)

    def test_post_already_restored(self):
        """Ensure that it doesn't matter if the configuration is not archived at the beginning."""
        self.configuration.archived = False
        db.session.add(self.configuration)
        db.session.commit()

        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.configuration.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_configuration = (
            db.session.query(Configuration).filter_by(id=self.configuration.id).one()
        )
        self.assertFalse(reloaded_configuration.archived)
        # But we don't change the entity
        self.assertEqual(reloaded_configuration.update_description, "create;basic data")
        self.assertIsNone(reloaded_configuration.updated_by_id)

    def test_post_site_archived(self):
        """Ensure to allow restoring when an associated site is archvived."""
        site = Site(label="site", is_public=True, is_internal=False, archived=True)
        self.configuration.site = site
        db.session.add_all([site, self.configuration])

        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.configuration.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
