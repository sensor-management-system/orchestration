# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the permission handling for configuration attachment resources."""

import json
from unittest.mock import patch

from project import base_url
from project.api.models import Configuration, ConfigurationAttachment, Contact, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list
from project.tests.permissions import create_a_test_configuration
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


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
        configuration = create_a_test_configuration(
            IDL_USER_ACCOUNT.membered_permission_groups[0]
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
        payload = prepare_configuration_attachment_payload(configuration)
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:

                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
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
        configuration = create_a_test_configuration(
            IDL_USER_ACCOUNT.membered_permission_groups[0]
        )
        configuration.archived = True
        db.session.add(configuration)
        db.session.commit()
        payload = prepare_configuration_attachment_payload(configuration)
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:

                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_post_to_a_configuration_with_an_other_permission_group(self):
        """Post to a configuration with a different permission Group from the user."""
        configuration = create_a_test_configuration(403)
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
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_a_configuration_with_a_permission_group(self):
        """Patch attachment of configuration with same group as user."""
        configuration = create_a_test_configuration(
            IDL_USER_ACCOUNT.membered_permission_groups[0]
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
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.patch(
                    url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(attachment.label, data["data"]["attributes"]["label"])
        self.assertEqual(attachment.url, data["data"]["attributes"]["url"])
        self.assertEqual(attachment.configuration_id, configuration.id)

    def test_patch_to_archived_configuration(self):
        """Ensure that we can't patch if the configuration is archived."""
        configuration = create_a_test_configuration(
            IDL_USER_ACCOUNT.membered_permission_groups[0]
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
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.patch(
                    url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_to_a_configuration_with_a_permission_group(self):
        """Delete attachment of configuration with same group as user (user is admin)."""
        configuration = create_a_test_configuration(
            IDL_USER_ACCOUNT.administrated_permission_groups[0]
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
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

    def test_delete_for_archived_configuration(self):
        """Ensure we can't delete for an archived configuration."""
        configuration = create_a_test_configuration(
            IDL_USER_ACCOUNT.administrated_permission_groups[0]
        )
        attachment = ConfigurationAttachment(
            label=fake.pystr(),
            url=fake.url(),
            configuration=configuration,
        )
        configuration.archived = True
        db.session.add_all([attachment, configuration])
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_to_a_configuration_with_a_permission_group_as_a_member(self):
        """Delete attachment of configuration with same group as user (user is member)."""
        configuration = create_a_test_configuration(
            IDL_USER_ACCOUNT.membered_permission_groups[0]
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
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
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
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
        )
        configuration1.cfg_permission_group = "1"
        configuration2 = create_a_test_configuration(
            public=False,
            internal=True,
        )
        configuration2.cfg_permission_group = "2"
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
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[configuration1.cfg_permission_group],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.url}/{attachment.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)
