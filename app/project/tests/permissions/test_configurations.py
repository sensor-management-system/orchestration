"""Tests for the Configuration-Permissions."""
import json
from unittest.mock import patch

from project import base_url
from project.api.models import User, Configuration
from project.api.models.base_model import db
from project.api.services.idl_services import Idl
from project.tests.base import BaseTestCase
from project.tests.base import create_token
from project.tests.base import fake
from project.tests.permissions import create_a_test_device, create_a_test_contact
from project.tests.permissions import create_superuser_token
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


class TestConfigurationPermissions(BaseTestCase):
    """Tests for the configuration Permissions."""

    configuration_url = base_url + "/configurations"
    object_type = "configuration"

    def test_add_public_configuration(self):
        """Ensure a new configuration can be public."""
        public_config = Configuration(
            id=15, label="public configuration", is_public=True, is_internal=False,
        )
        db.session.add(public_config)
        db.session.commit()

        configuration = (
            db.session.query(Configuration).filter_by(id=public_config.id).one()
        )
        self.assertEqual(configuration.is_public, True)
        self.assertEqual(configuration.is_internal, False)

    def test_add_configuration_model(self):
        """Ensure a new configuration model can be internal."""
        internal_config = Configuration(
            id=33, label="internal configuration", is_internal=True, is_public=False,
        )
        db.session.add(internal_config)
        db.session.commit()

        configuration = (
            db.session.query(Configuration).filter_by(id=internal_config.id).one()
        )
        self.assertEqual(configuration.is_internal, True)
        self.assertEqual(configuration.is_public, False)

    def test_add_configuration(self):
        """Ensure a new configuration can be added to api and is internal."""
        configuration_data = {
            "data": {
                "type": "configuration",
                "attributes": {
                    "label": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "cfg_permission_group": "1",
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.configuration_url,
                data=json.dumps(configuration_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["data"]["attributes"]["is_internal"], True)
        self.assertEqual(data["data"]["attributes"]["is_public"], False)

    def test_get_all_as_anonymous_user(self):
        """Ensure anonymous user can only see public objects."""
        public_config = Configuration(
            id=15, label=fake.pystr(), is_internal=False, is_public=True
        )

        internal_config = Configuration(
            id=33, label=fake.pystr(), is_public=False, is_internal=True
        )

        db.session.add_all([public_config, internal_config])
        db.session.commit()

        response = self.client.get(self.configuration_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["id"], str(public_config.id))

    def test_get_an_internal_config_as_anonymous_user(self):
        """Ensure anonymous user can't access an internal configuration."""
        internal_config = Configuration(
            label=fake.pystr(), is_public=False, is_internal=True
        )

        db.session.add(internal_config)
        db.session.commit()
        url = f"{self.configuration_url}/{internal_config.id}"
        response = self.client.get(url)
        self.assertNotEqual(response.status, 200)

    def test_get_as_registered_user(self):
        """Ensure that a registered user can see public, internal, and only his own private objects"""
        public_config = Configuration(
            id=15, label=fake.pystr(), is_public=True, is_internal=False,
        )

        internal_config = Configuration(
            id=33, label=fake.pystr(), is_public=False, is_internal=True,
        )

        contact = create_a_test_contact()
        contact_1 = create_a_test_device()

        user = User(subject="test_user@test.test", contact=contact)
        user_1 = User(subject="test_user1@test.test", contact=contact_1)
        db.session.add_all(
            [public_config, internal_config, contact, user, contact_1, user_1]
        )
        db.session.commit()

        token_data = {
            "sub": user.subject,
            "iss": "SMS unittest",
            "family_name": contact.family_name,
            "given_name": contact.given_name,
            "email": contact.email,
            "aud": "SMS",
        }
        access_headers = create_token(token_data)
        response = self.client.get(self.configuration_url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 2)

    def test_add_configuration_with_multiple_true_permission_values(self):
        """Make sure that a configuration can't have multiple True permission values at the same time"""
        configuration_data = {
            "data": {
                "type": "configuration",
                "attributes": {
                    "label": fake.pystr(),
                    "is_public": True,
                    "is_internal": True,
                    "cfg_permission_group": IDL_USER_ACCOUNT.membered_permission_groups[
                        0
                    ],
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.configuration_url,
                data=json.dumps(configuration_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_add_groups_ids(self):
        """Make sure that a configuration with groups-ids can be created"""
        config_data = {
            "data": {
                "type": "configuration",
                "attributes": {
                    "label": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "cfg_permission_group": "12",
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.configuration_url,
                data=json.dumps(config_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        self.assertEqual(data["data"]["attributes"]["cfg_permission_group"], "12")

    def test_patch_configuration_as_a_member_in_a_permission_group(self):
        """Make sure that a member in a group (admin/member) can change
         the configuration data per patch request"""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups[
            0
        ]
        configs = preparation_of_public_and_internal_configuration_data(
            group_id_test_user_is_member_in_2
        )
        access_headers = create_token()
        for configuration_data in configs:
            with self.client:
                response = self.client.post(
                    self.configuration_url,
                    data=json.dumps(configuration_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertIn(
                group_id_test_user_is_member_in_2[0],
                data["data"]["attributes"]["cfg_permission_group"],
            )
            with patch.object(
                    Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                configuration_data_changed = {
                    "data": {
                        "type": "configuration",
                        "id": data["data"]["id"],
                        "attributes": {"label": "Changed configuration name"},
                    }
                }
                url = f"{self.configuration_url}/{data['data']['id']}"
                res = super().update_object(
                    url, configuration_data_changed, self.object_type
                )
                self.assertEqual(
                    res["data"]["attributes"]["label"],
                    configuration_data_changed["data"]["attributes"]["label"],
                )

    def test_patch_configuration_user_not_in_any_permission_group(self):
        """Make sure that a user can only do changes in configurations, where he/she is involved."""
        group_id_test_user_is_not_included = "13"
        configs = preparation_of_public_and_internal_configuration_data(
            group_id_test_user_is_not_included
        )
        access_headers = create_token()
        for configuration_data in configs:
            with self.client:
                response = self.client.post(
                    self.configuration_url,
                    data=json.dumps(configuration_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertEqual(
                data["data"]["attributes"]["cfg_permission_group"],
                group_id_test_user_is_not_included,
            )
            with patch.object(
                    Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                configuration_data_changed_forbidden = {
                    "data": {
                        "type": "configuration",
                        "id": data["data"]["id"],
                        "attributes": {"label": "Forbidden"},
                    }
                }
                url = f"{self.configuration_url}/{data['data']['id']}"
                access_headers = create_token()
                with self.client:
                    response = self.client.patch(
                        url,
                        data=json.dumps(configuration_data_changed_forbidden),
                        content_type="application/vnd.api+json",
                        headers=access_headers,
                    )
                self.assertEqual(response.status, "403 FORBIDDEN")

    def test_delete_configuration_as_not_an_admin_in_a_permission_group(self):
        """Make sure that only admin can delete a configuration in the same permission group."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups[
            0
        ]
        configs = preparation_of_public_and_internal_configuration_data(
            group_id_test_user_is_member_in_2
        )
        access_headers = create_token()
        for configuration_data in configs:
            with self.client:
                response = self.client.post(
                    self.configuration_url,
                    data=json.dumps(configuration_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertIn(
                group_id_test_user_is_member_in_2[0],
                data["data"]["attributes"]["cfg_permission_group"],
            )
            with patch.object(
                    Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                url = f"{self.configuration_url}/{data['data']['id']}"
                delete_response = self.client.delete(url, headers=access_headers)
                delete_data = json.loads(delete_response.data.decode())
                self.assertEqual(delete_data["errors"][0]["status"], 409)

    def test_delete_configuration_as_an_admin_in_a_permission_group(self):
        """Make sure that permission group admins are allowed to delete a configuration"""
        group_id_test_user_is_admin_in_1 = IDL_USER_ACCOUNT.administrated_permission_groups[
            0
        ]
        configs = preparation_of_public_and_internal_configuration_data(
            group_id_test_user_is_admin_in_1
        )
        access_headers = create_token()
        for configuration_data in configs:
            with self.client:
                response = self.client.post(
                    self.configuration_url,
                    data=json.dumps(configuration_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertEqual(
                data["data"]["attributes"]["cfg_permission_group"],
                IDL_USER_ACCOUNT.administrated_permission_groups[0],
            )

            with patch.object(
                    Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                url = f"{self.configuration_url}/{data['data']['id']}"
                delete_response = self.client.delete(url, headers=access_headers)
                self.assertEqual(delete_response.status_code, 200)

    def test_delete_configuration_as_super_user(self):
        """Make sure that a superuser can delete a configuration even if he/she is not admin in
        the corresponding permission group."""
        group_id_test_user_is_not_included = "20"
        configs = preparation_of_public_and_internal_configuration_data(
            group_id_test_user_is_not_included
        )
        access_headers = create_superuser_token()
        for configuration_data in configs:
            with self.client:
                response = self.client.post(
                    self.configuration_url,
                    data=json.dumps(configuration_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertEqual(
                data["data"]["attributes"]["cfg_permission_group"],
                group_id_test_user_is_not_included,
            )

            with patch.object(
                    Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                url = f"{self.configuration_url}/{data['data']['id']}"
                delete_response = self.client.delete(url, headers=access_headers)
                self.assertEqual(delete_response.status_code, 200)


def preparation_of_public_and_internal_configuration_data(group_id):
    """
    Data to add an internal and a public configuration.

    :param group_id: one permission group
    :return: list of data for two configs [public, internal]
    """
    public_configuration_data = {
        "data": {
            "type": "configuration",
            "attributes": {
                "label": fake.pystr(),
                "is_public": True,
                "is_internal": False,
                "cfg_permission_group": group_id,
            },
        }
    }
    internal_configuration_data = {
        "data": {
            "type": "configuration",
            "attributes": {
                "label": fake.pystr(),
                "is_public": False,
                "is_internal": True,
                "cfg_permission_group": group_id,
            },
        }
    }
    configs = [public_configuration_data, internal_configuration_data]
    return configs
