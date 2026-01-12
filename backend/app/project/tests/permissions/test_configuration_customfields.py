# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the custom field endpoints."""

import json

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationCustomField,
    Contact,
    PermissionGroup,
    PermissionGroupMembership,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list


def prepare_configuration_custom_field_payload(configuration):
    """Create some payload to send to the backend."""
    payload = {
        "data": {
            "type": "configuration_customfield",
            "attributes": {
                "value": fake.pystr(),
                "key": fake.pystr(),
            },
            "relationships": {
                "configuration": {
                    "data": {"type": "configuration", "id": str(configuration.id)}
                }
            },
        }
    }
    return payload


class TestConfigurationCustomFieldServices(BaseTestCase):
    """Test the configuration customfields."""

    url = base_url + "/configuration-customfields"

    def setUp(self):
        """Set stuff up for the tests."""
        super().setUp()
        normal_contact = Contact(
            given_name="normal", family_name="user", email="normal.user@localhost"
        )
        self.normal_user = User(subject=normal_contact.email, contact=normal_contact)
        self.permission_group = PermissionGroup(name="test", entitlement="test")
        self.other_group = PermissionGroup(name="other", entitlement="other")
        self.membership = PermissionGroupMembership(
            permission_group=self.permission_group, user=self.normal_user
        )
        db.session.add_all(
            [
                normal_contact,
                self.normal_user,
                self.permission_group,
                self.other_group,
                self.membership,
            ]
        )
        db.session.commit()

    def test_get_public_customfields(self):
        """Ensure that we can get a list of public customfields."""
        configuration1 = Configuration(
            label=fake.pystr(),
            is_public=True,
            is_internal=False,
        )
        configuration2 = Configuration(
            label=fake.pystr(),
            is_public=True,
            is_internal=False,
        )

        db.session.add(configuration1)
        db.session.add(configuration2)
        db.session.commit()

        customfield1 = ConfigurationCustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            configuration=configuration1,
        )
        customfield2 = ConfigurationCustomField(
            key="UFZ",
            value="https://www.ufz.de",
            configuration=configuration1,
        )
        customfield3 = ConfigurationCustomField(
            key="PIK",
            value="https://www.pik-potsdam.de",
            configuration=configuration2,
        )

        db.session.add(customfield1)
        db.session.add(customfield2)
        db.session.add(customfield3)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url + "/configuration-customfields",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

    def test_get_internal_customfields(self):
        """Ensure that we can get a list of internal customfields only with a valid jwt."""
        configuration1 = Configuration(
            label=fake.pystr(),
            is_public=False,
            is_internal=True,
        )
        configuration2 = Configuration(
            label=fake.pystr(),
            is_public=False,
            is_internal=True,
        )

        db.session.add(configuration1)
        db.session.add(configuration2)
        db.session.commit()

        customfield1 = ConfigurationCustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            configuration=configuration1,
        )
        customfield2 = ConfigurationCustomField(
            key="UFZ",
            value="https://www.ufz.de",
            configuration=configuration1,
        )

        db.session.add(customfield1)
        db.session.add(customfield2)
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
        """Post to configuration, with permission group."""
        configuration = Configuration(
            label=fake.pystr(),
            is_public=False,
            is_internal=True,
            cfg_permission_group=str(self.permission_group.id),
        )
        db.session.add(configuration)
        db.session.commit()
        self.assertTrue(configuration.id is not None)
        count_customfields = (
            db.session.query(ConfigurationCustomField)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )

        self.assertEqual(count_customfields, 0)
        payload = prepare_configuration_custom_field_payload(configuration)
        with self.run_requests_as(self.normal_user):
            url_post = base_url + "/configuration-customfields"

            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        self.assertEqual(response.status_code, 201)
        customfields = query_result_to_list(
            db.session.query(ConfigurationCustomField).filter_by(
                configuration_id=configuration.id,
            )
        )
        self.assertEqual(len(customfields), 1)

        customfield = customfields[0]
        self.assertEqual(customfield.value, payload["data"]["attributes"]["value"])
        self.assertEqual(customfield.key, payload["data"]["attributes"]["key"])
        self.assertEqual(customfield.configuration_id, configuration.id)

        self.assertEqual(
            str(customfield.configuration_id),
            response.get_json()["data"]["relationships"]["configuration"]["data"]["id"],
        )

    def test_post_for_archived_configuration(self):
        """Ensure we can't post for an archived configuration."""
        configuration = Configuration(
            label=fake.pystr(),
            is_public=False,
            is_internal=True,
            cfg_permission_group=str(self.permission_group.id),
            archived=True,
        )
        db.session.add(configuration)
        db.session.commit()
        payload = prepare_configuration_custom_field_payload(configuration)
        with self.run_requests_as(self.normal_user):
            url_post = base_url + "/configuration-customfields"

            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        self.assertEqual(response.status_code, 403)

    def test_post_to_a_configuration_with_an_other_permission_group(self):
        """Post to a configuration with a different permission group from the user."""
        configuration = Configuration(
            label=fake.pystr(),
            is_public=False,
            is_internal=True,
            cfg_permission_group=str(self.other_group.id),
        )
        db.session.add(configuration)
        db.session.commit()
        self.assertTrue(configuration.id is not None)
        count_customfields = (
            db.session.query(ConfigurationCustomField)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )

        self.assertEqual(count_customfields, 0)
        payload = prepare_configuration_custom_field_payload(configuration)
        with self.run_requests_as(self.normal_user):
            url_post = base_url + "/configuration-customfields"

            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        self.assertEqual(response.status_code, 403)

    def test_patch_to_a_configuration_with_a_permission_group(self):
        """Patch custom field attached to configuration with same group as user."""
        configuration = Configuration(
            label=fake.pystr(),
            is_public=False,
            is_internal=True,
            cfg_permission_group=str(self.permission_group.id),
        )
        db.session.add(configuration)
        db.session.commit()
        self.assertTrue(configuration.id is not None)
        count_customfields = (
            db.session.query(ConfigurationCustomField)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )

        self.assertEqual(count_customfields, 0)
        customfield = ConfigurationCustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            configuration=configuration,
        )
        db.session.add(customfield)
        db.session.commit()
        payload = {
            "data": {
                "id": customfield.id,
                "type": "configuration_customfield",
                "attributes": {"value": "changed", "key": customfield.key},
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": str(configuration.id)}
                    }
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            url = base_url + "/configuration-customfields/" + str(customfield.id)

            response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(customfield.value, data["data"]["attributes"]["value"])
        self.assertEqual(customfield.key, data["data"]["attributes"]["key"])
        self.assertEqual(customfield.configuration_id, configuration.id)

    def test_patch_for_archived_configuration(self):
        """Ensure we can't patch for an archived configuration."""
        configuration = Configuration(
            label=fake.pystr(),
            is_public=False,
            is_internal=True,
            cfg_permission_group=str(self.permission_group.id),
            archived=True,
        )
        db.session.add(configuration)
        db.session.commit()
        customfield = ConfigurationCustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            configuration=configuration,
        )
        db.session.add(customfield)
        db.session.commit()
        payload = {
            "data": {
                "id": customfield.id,
                "type": "configuration_customfield",
                "attributes": {"value": "changed", "key": customfield.key},
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": str(configuration.id)}
                    }
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            url = base_url + "/configuration-customfields/" + str(customfield.id)

            response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        self.assertEqual(response.status_code, 403)

    def test_delete_for_a_configuration_with_a_permission_group(self):
        """Delete customfield for configuration with same group as user (admin)."""
        configuration = Configuration(
            label=fake.pystr(),
            is_public=False,
            is_internal=True,
            cfg_permission_group=str(self.permission_group.id),
        )
        db.session.add(configuration)
        db.session.commit()
        self.assertTrue(configuration.id is not None)
        count_customfields = (
            db.session.query(ConfigurationCustomField)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )

        self.assertEqual(count_customfields, 0)
        customfield = ConfigurationCustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            configuration=configuration,
        )
        db.session.add(customfield)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            url = base_url + "/configuration-customfields/" + str(customfield.id)

            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)
        reloaded_configuration = (
            db.session.query(Configuration).filter_by(id=configuration.id).first()
        )
        self.assertEqual(
            reloaded_configuration.update_description, "delete;custom field"
        )

    def test_delete_for_archived_configuration(self):
        """Ensure we can't delete for an archived configuration."""
        configuration = Configuration(
            label=fake.pystr(),
            is_public=False,
            is_internal=True,
            cfg_permission_group=str(self.permission_group.id),
            archived=True,
        )
        db.session.add(configuration)
        db.session.commit()
        customfield = ConfigurationCustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            configuration=configuration,
        )
        db.session.add(customfield)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            url = base_url + "/configuration-customfields/" + str(customfield.id)

            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_non_editable_configuration(self):
        """Ensure we can't update to a configuration we can't edit."""
        configuration1 = Configuration(
            label="config1",
            is_public=False,
            is_internal=True,
            cfg_permission_group=str(self.permission_group.id),
        )
        configuration2 = Configuration(
            label="config2",
            is_public=False,
            is_internal=True,
            cfg_permission_group=str(self.other_group.id),
        )
        custom_field = ConfigurationCustomField(
            key="k",
            value="v",
            configuration=configuration1,
        )
        db.session.add_all([configuration1, configuration2, custom_field])
        db.session.commit()

        payload = {
            "data": {
                "type": "configuration_customfield",
                "id": custom_field.id,
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

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.url}/{custom_field.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)
