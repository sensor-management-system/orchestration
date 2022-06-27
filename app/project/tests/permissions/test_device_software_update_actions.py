"""Tests for the device software update action api."""

import json
from unittest.mock import patch

from project import base_url
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake
from project.tests.models.test_software_update_actions_model import (
    add_device_software_update_action_model,
)
from project.tests.permissions import create_a_test_contact
from project.tests.permissions.test_customfields import create_a_test_device
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def prepare_software_update_action_payload(object_type, device, contact):
    data = {
        "data": {
            "type": object_type,
            "attributes": {
                "description": "Test DeviceCalibrationAction",
                "version": f"v_{fake.pyint()}",
                "software_type_name": fake.pystr(),
                "software_type_uri": fake.uri(),
                "repository_url": fake.url(),
                "update_date": fake.future_datetime().__str__(),
            },
            "relationships": {
                "device": {"data": {"type": "device", "id": device.id}},
                "contact": {"data": {"type": "contact", "id": contact.id}},
            },
        }
    }
    return data


class TestDeviceSoftwareUpdateAction(BaseTestCase):
    """Tests for the DeviceSoftwareUpdateAction endpoints."""

    url = base_url + "/device-software-update-actions"
    object_type = "device_software_update_action"

    def test_get_device_software_update_action_collection(self):
        """Test retrieve a collection of public DeviceSoftwareUpdateAction objects."""
        sau = add_device_software_update_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(sau.description, data["data"][0]["attributes"]["description"])

    def test_get_internal_device_software_update_action_collection(self):
        """Test retrieve a collection of internal DeviceSoftwareUpdateAction objects."""
        _ = add_device_software_update_action_model(
            public=False, private=False, internal=True
        )
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_post_action_with_a_permission_group(self):
        """Post to device,with permission Group."""
        device = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(device.id is not None)
        contact = create_a_test_contact()
        payload = prepare_software_update_action_payload(
            self.object_type, device, contact
        )
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

    def test_post_action__user_not_in_the_permission_group(self):
        """Post to device,with permission Group different from the user group."""
        device = create_a_test_device([403])
        self.assertTrue(device.id is not None)
        contact = create_a_test_contact()
        payload = prepare_software_update_action_payload(
            self.object_type, device, contact
        )
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,contact",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_patch_action_with_a_permission_group(self):
        """Post to device,with permission Group."""
        device_software_update_action = add_device_software_update_action_model(
            group_ids=IDL_USER_ACCOUNT.membered_permission_groups
        )
        self.assertTrue(device_software_update_action.id is not None)
        device_software_update_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_software_update_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{device_software_update_action.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.patch(
                    url,
                    data=json.dumps(device_software_update_action_updated),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

    def test_patch_action__user_is_not_part_from_permission_group(self):
        """Post to device,with permission Group."""
        device_software_update_action = add_device_software_update_action_model(
            group_ids=[403]
        )
        self.assertTrue(device_software_update_action.id is not None)
        device_software_update_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_software_update_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{device_software_update_action.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.patch(
                    url,
                    data=json.dumps(device_software_update_action_updated),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_software_update_action(self):
        """Delete DeviceSoftwareUpdateAction."""
        device_software_update_action = add_device_software_update_action_model(
            group_ids=IDL_USER_ACCOUNT.administrated_permission_groups
        )
        url = f"{self.url}/{device_software_update_action.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

    def test_delete_software_update_action_as_member(self):
        """Delete DeviceSoftwareUpdateAction as member."""
        device_software_update_action = add_device_software_update_action_model(
            group_ids=IDL_USER_ACCOUNT.membered_permission_groups
        )
        url = f"{self.url}/{device_software_update_action.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)
