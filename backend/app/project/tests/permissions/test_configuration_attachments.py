# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the permission handling for configuration attachment resources."""

import json

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationAttachment,
    Contact,
    PermissionGroup,
    PermissionGroupMembership,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list
from project.tests.permissions import create_a_test_configuration


def prepare_configuration_attachment_payload(configuration):
    """Create some test payload for configuration attachments."""
    payload = {
        "data": {
            "type": "configuration_attachment",
            "attributes": {"label": fake.pystr(), "url": fake.url()},
            "relationships": {
                "configuration": {
                    "data": {"type": "configuration", "id": str(configuration.id)}
                }
            },
        }
    }
    return payload


class TestConfigurationAttachment(BaseTestCase):
    """Test ConfigurationAttachment."""

    url = base_url + "/configuration-attachments"

    def setUp(self):
        """Set stuff up for the tests."""
        super().setUp()
        normal_contact = Contact(
            given_name="normal", family_name="user", email="normal.user@localhost"
        )
        self.normal_user = User(subject=normal_contact.email, contact=normal_contact)
        db.session.add_all([normal_contact, self.normal_user])
        db.session.commit()

    def test_get_public_configuration_attachments(self):
        """Ensure that we can get a list of public configuration_attachments."""
        configuration1 = create_a_test_configuration(
            public=True,
            internal=False,
        )
        configuration2 = create_a_test_configuration(
            public=True,
            internal=False,
        )

        attachment1 = ConfigurationAttachment(
            label=fake.pystr(),
            url=fake.url(),
            configuration=configuration1,
        )
        attachment2 = ConfigurationAttachment(
            label=fake.pystr(),
            url=fake.url(),
            configuration=configuration1,
        )
        attachment3 = ConfigurationAttachment(
            label=fake.pystr(),
            url=fake.url(),
            configuration=configuration2,
        )

        db.session.add_all([attachment1, attachment2, attachment3])
        db.session.commit()

        with self.client:
            response = self.client.get(
                self.url,
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

    def test_get_internal_configuration_attachments(self):
        """Ensure that we get internal configuration attachments only for authenticate users."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
        )
        configuration2 = create_a_test_configuration(
            public=False,
            internal=True,
        )

        attachment1 = ConfigurationAttachment(
            label=fake.pystr(),
            url=fake.url(),
            configuration=configuration1,
        )
        attachment2 = ConfigurationAttachment(
            label=fake.pystr(),
            url=fake.url(),
            configuration=configuration2,
        )

        db.session.add_all([attachment1, attachment2])
        db.session.commit()

        with self.client:
            response = self.client.get(
                self.url,
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

    def test_post_to_a_configuration_with_a_permission_group(self):
        """Post to configuration,with permission Group."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()

        configuration = create_a_test_configuration(str(permission_group.id))
        self.assertTrue(configuration.id is not None)
        count_configuration_attachments = (
            db.session.query(ConfigurationAttachment)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )

        self.assertEqual(count_configuration_attachments, 0)
        payload = prepare_configuration_attachment_payload(configuration)
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 201)
        configuration_attachments = query_result_to_list(
            db.session.query(ConfigurationAttachment).filter_by(
                configuration_id=configuration.id,
            )
        )
        self.assertEqual(len(configuration_attachments), 1)

        attachment = configuration_attachments[0]
        self.assertEqual(attachment.label, payload["data"]["attributes"]["label"])
        self.assertEqual(attachment.url, payload["data"]["attributes"]["url"])
        self.assertEqual(attachment.configuration_id, configuration.id)
        self.assertEqual(
            str(attachment.configuration_id), response.get_json()["data"]["id"]
        )

    def test_post_to_archived_configuration(self):
        """Ensure that we can't post for an archived configuration."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()
        configuration = create_a_test_configuration(
            str(permission_group.id),
        )
        configuration.archived = True
        db.session.add(configuration)
        db.session.commit()
        payload = prepare_configuration_attachment_payload(configuration)

        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_post_to_a_configuration_with_an_other_permission_group(self):
        """Post to a configuration with a different permission Group from the user."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        other_group = PermissionGroup(name="other", entitlement="other")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, other_group, membership])
        db.session.commit()
        configuration = create_a_test_configuration(str(other_group.id))
        self.assertTrue(configuration.id is not None)
        count_configuration_attachments = (
            db.session.query(ConfigurationAttachment)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )

        self.assertEqual(count_configuration_attachments, 0)
        payload = prepare_configuration_attachment_payload(configuration)
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_a_configuration_with_a_permission_group(self):
        """Patch attachment of configuration with same group as user."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()

        configuration = create_a_test_configuration(
            str(permission_group.id),
        )
        self.assertTrue(configuration.id is not None)
        count_configuration_attachments = (
            db.session.query(ConfigurationAttachment)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )

        self.assertEqual(count_configuration_attachments, 0)
        attachment = ConfigurationAttachment(
            label=fake.pystr(),
            url=fake.url(),
            configuration=configuration,
        )
        db.session.add(attachment)
        db.session.commit()
        payload = {
            "data": {
                "id": attachment.id,
                "type": "configuration_attachment",
                "attributes": {"label": "changed", "url": attachment.url},
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": str(configuration.id)}
                    }
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(attachment.label, data["data"]["attributes"]["label"])
        self.assertEqual(attachment.url, data["data"]["attributes"]["url"])
        self.assertEqual(attachment.configuration_id, configuration.id)

    def test_patch_to_archived_configuration(self):
        """Ensure that we can't patch if the configuration is archived."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()
        configuration = create_a_test_configuration(
            str(permission_group.id),
        )
        attachment = ConfigurationAttachment(
            label=fake.pystr(),
            url=fake.url(),
            configuration=configuration,
        )
        configuration.archived = True
        db.session.add_all([attachment, configuration])
        db.session.commit()
        payload = {
            "data": {
                "id": attachment.id,
                "type": "configuration_attachment",
                "attributes": {"label": "changed", "url": attachment.url},
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": str(configuration.id)}
                    }
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_to_a_configuration_with_a_permission_group(self):
        """Delete attachment of configuration with same group as user (user is admin)."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()
        configuration = create_a_test_configuration(
            str(permission_group.id),
        )
        self.assertTrue(configuration.id is not None)
        count_configuration_attachments = (
            db.session.query(ConfigurationAttachment)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )

        self.assertEqual(count_configuration_attachments, 0)
        attachment = ConfigurationAttachment(
            label=fake.pystr(),
            url=fake.url(),
            configuration=configuration,
        )
        db.session.add(attachment)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_for_archived_configuration(self):
        """Ensure we can't delete for an archived configuration."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()

        configuration = create_a_test_configuration(
            str(permission_group.id),
        )
        attachment = ConfigurationAttachment(
            label=fake.pystr(),
            url=fake.url(),
            configuration=configuration,
        )
        configuration.archived = True
        db.session.add_all([attachment, configuration])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_to_a_configuration_with_a_permission_group_as_a_member(self):
        """Delete attachment of configuration with same group as user (user is member)."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()

        configuration = create_a_test_configuration(
            str(permission_group.id),
        )
        self.assertTrue(configuration.id is not None)
        count_configuration_attachments = (
            db.session.query(ConfigurationAttachment)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )

        self.assertEqual(count_configuration_attachments, 0)
        attachment = ConfigurationAttachment(
            label=fake.pystr(),
            url=fake.url(),
            configuration=configuration,
        )
        db.session.add(attachment)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)
        configuration_reloaded = (
            db.session.query(Configuration)
            .filter_by(
                id=configuration.id,
            )
            .first()
        )
        self.assertEqual(configuration_reloaded.update_description, "delete;attachment")

    def test_patch_to_non_editable_configuration(self):
        """Ensure we can't update to a configuration we can't edit."""
        permission_group1 = PermissionGroup(name="test", entitlement="test")
        permission_group2 = PermissionGroup(name="test2", entitlement="test2")
        db.session.add_all([permission_group1, permission_group2])
        db.session.commit()

        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
        )
        configuration1.cfg_permission_group = str(permission_group1.id)
        configuration2 = create_a_test_configuration(
            public=False,
            internal=True,
        )
        configuration2.cfg_permission_group = str(permission_group2.id)
        attachment = ConfigurationAttachment(
            url="https://gfz.potsdam.de",
            label="gfz",
            configuration=configuration1,
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all([configuration1, configuration2, contact, user, attachment])
        db.session.commit()

        payload = {
            "data": {
                "type": "configuration_attachment",
                "id": attachment.id,
                "attributes": {},
                "relationships": {
                    # We try to switch here to another configuration for
                    # which we have no edit permissions.
                    "configuration": {
                        "data": {
                            "type": "configuration",
                            "id": configuration2.id,
                        }
                    },
                },
            }
        }

        with self.run_requests_as(user):
            response = self.client.patch(
                f"{self.url}/{attachment.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)
