"""Tests for the platform software update actions api."""
import json
from unittest.mock import patch

from project import base_url
from project.api.services.idl_services import Idl
from project.tests.base import BaseTestCase, fake
from project.tests.base import create_token
from project.tests.models.test_software_update_actions_model import (
    add_platform_software_update_action_model,
)
from project.tests.permissions import create_a_test_platform, create_a_test_device
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def prepare_software_update_action_payload(object_type, platform, contact):
    data = {
        "data": {
            "type": object_type,
            "attributes": {
                "description": "Test platform_software_update_action",
                "version": f"v_{fake.pyint()}",
                "software_type_name": fake.pystr(),
                "software_type_uri": fake.uri(),
                "repository_url": fake.url(),
                "update_date": fake.future_datetime().__str__(),
            },
            "relationships": {
                "platform": {"data": {"type": "platform", "id": platform.id}},
                "contact": {"data": {"type": "contact", "id": contact.id}},
            },
        }
    }
    return data


class TestPlatformSoftwareUpdateAction(BaseTestCase):
    """Tests for the PlatformSoftwareUpdateAction endpoints."""

    url = base_url + "/platform-software-update-actions"
    object_type = "platform_software_update_action"

    def test_get_platform_software_update_action_collection(self):
        """Test retrieve a collection of public PlatformSoftwareUpdateAction objects."""
        sau = add_platform_software_update_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(sau.description, data["data"][0]["attributes"]["description"])

    def test_get_internal_platform_software_update_action_collection(self):
        """Test retrieve a collection of internal PlatformSoftwareUpdateAction objects."""
        _ = add_platform_software_update_action_model(
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
        platform = create_a_test_platform(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(platform.id is not None)
        contact = create_a_test_device()
        payload = prepare_software_update_action_payload(
            self.object_type, platform, contact
        )
        with patch.object(
                Idl, "get_all_permission_groups_for_a_user"
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
        platform = create_a_test_platform([403])
        self.assertTrue(platform.id is not None)
        contact = create_a_test_device()
        payload = prepare_software_update_action_payload(
            self.object_type, platform, contact
        )
        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
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
        device_software_update_action = add_platform_software_update_action_model(
            group_ids=IDL_USER_ACCOUNT.membered_permission_groups
        )
        self.assertTrue(device_software_update_action.id is not None)
        device_software_update_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_software_update_action.id,
                "attributes": {"description": "updated",},
            }
        }
        url = f"{self.url}/{device_software_update_action.id}"
        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
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
        device_software_update_action = add_platform_software_update_action_model(
            group_ids=[403]
        )
        self.assertTrue(device_software_update_action.id is not None)
        device_software_update_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_software_update_action.id,
                "attributes": {"description": "updated",},
            }
        }
        url = f"{self.url}/{device_software_update_action.id}"
        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
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
        device_software_update_action = add_platform_software_update_action_model(
            group_ids=IDL_USER_ACCOUNT.administrated_permission_groups
        )
        url = f"{self.url}/{device_software_update_action.id}"
        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
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
        device_software_update_action = add_platform_software_update_action_model(
            group_ids=IDL_USER_ACCOUNT.membered_permission_groups
        )
        url = f"{self.url}/{device_software_update_action.id}"
        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)