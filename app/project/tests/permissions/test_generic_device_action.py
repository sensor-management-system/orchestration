"""Tests for the generic device actions api."""
import json
from datetime import datetime
from unittest.mock import patch

from project import base_url, db
from project.api.models import Device, GenericDeviceAction
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake
from project.tests.models.test_generic_actions_models import (
    generate_device_action_model,
)
from project.tests.permissions import create_a_test_contact, create_a_test_device
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def make_generic_device_action_data(object_type, group_ids=None):
    """
    Create the json payload for a generic device action.

    This also creates some associated objects in the database.
    """
    if not group_ids:
        group_ids = []
    device = create_a_test_device(group_ids)
    contact = create_a_test_contact()

    data = {
        "data": {
            "type": object_type,
            "attributes": {
                "description": fake.paragraph(nb_sentences=3),
                "action_type_name": fake.lexify(
                    text="Random type: ??????????", letters="ABCDE"
                ),
                "action_type_uri": fake.uri(),
                "begin_date": datetime.now().__str__(),
            },
            "relationships": {
                "device": {"data": {"type": "device", "id": device.id}},
                "contact": {"data": {"type": "contact", "id": contact.id}},
            },
        }
    }
    return data


class TestGenericDeviceActionPermissions(BaseTestCase):
    """Tests for the GenericDeviceAction permissions."""

    url = base_url + "/generic-device-actions"
    object_type = "generic_device_action"

    def test_a_public_generic_device_action(self):
        """Ensure a public generic device action will be listed."""
        generic_device_action = generate_device_action_model()
        action = (
            db.session.query(GenericDeviceAction)
            .filter_by(id=generic_device_action.id)
            .one()
        )
        self.assertEqual(action.description, generic_device_action.description)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_a_internal_generic_device_action(self):
        """Ensure an internal generic device action won't be listed for anonymous."""
        generic_device_action = generate_device_action_model(
            public=False, private=False, internal=True
        )
        action = (
            db.session.query(GenericDeviceAction)
            .filter_by(id=generic_device_action.id)
            .one()
        )
        self.assertEqual(action.description, generic_device_action.description)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_add_generic_device_action_with_a_permission_group(self):
        """Ensure POST a new generic device action can be added to the database."""
        payload = make_generic_device_action_data(
            self.object_type, group_ids=IDL_USER_ACCOUNT.membered_permission_groups
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

    def test_post_for_archived_device(self):
        """Ensure POST a new generic device action can be added to the database."""
        payload = make_generic_device_action_data(
            self.object_type, group_ids=IDL_USER_ACCOUNT.membered_permission_groups
        )
        device = db.session.query(Device).order_by("created_at").first()
        device.archived = True
        db.session.add(device)
        db.session.commit()

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
        self.assertEqual(response.status_code, 409)

    def test_post_generic_device_action_data_user_not_in_the_permission_group(self):
        """Post to device,with permission Group different from the user group."""
        payload = make_generic_device_action_data(self.object_type, group_ids=[403])
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

    def test_patch_action_with_a_permission_group(self):
        """Post to generic_device_action_data,with permission Group."""
        payload = generate_device_action_model(
            group_ids=IDL_USER_ACCOUNT.membered_permission_groups
        )
        self.assertTrue(payload.id is not None)
        generic_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": payload.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{payload.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.patch(
                    url,
                    data=json.dumps(generic_device_action_updated),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

    def test_patch_for_archived_device(self):
        """Ensure that we can't patch for archived devices."""
        payload = generate_device_action_model(
            group_ids=IDL_USER_ACCOUNT.membered_permission_groups
        )
        device = db.session.query(Device).order_by("created_at").first()
        device.archived = True
        db.session.add(device)
        db.session.commit()

        generic_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": payload.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{payload.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.patch(
                    url,
                    data=json.dumps(generic_device_action_updated),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 409)

    def test_patch_generic_device_action_data_user_is_not_part_from_permission_group(
        self,
    ):
        """Post to device,with permission Group."""
        generic_device_action = generate_device_action_model(group_ids=[403])
        self.assertTrue(generic_device_action.id is not None)
        generic_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": generic_device_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{generic_device_action.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.patch(
                    url,
                    data=json.dumps(generic_device_action_updated),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_generic_device_action_data(self):
        """Delete generic_device_action_data."""
        generic_device_action = generate_device_action_model(
            group_ids=IDL_USER_ACCOUNT.administrated_permission_groups
        )
        url = f"{self.url}/{generic_device_action.id}"
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

    def test_delete_for_archived_device(self):
        """Ensure we can't delete for archived devices."""
        generic_device_action = generate_device_action_model(
            group_ids=IDL_USER_ACCOUNT.administrated_permission_groups
        )
        device = db.session.query(Device).order_by("created_at").first()
        device.archived = True
        db.session.add(device)
        db.session.commit()
        url = f"{self.url}/{generic_device_action.id}"
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
        self.assertEqual(response.status_code, 409)

    def test_delete_generic_device_action_data_as_member(self):
        """Delete generic_device_action_data as member."""
        generic_device_action = generate_device_action_model(
            group_ids=IDL_USER_ACCOUNT.membered_permission_groups
        )
        url = f"{self.url}/{generic_device_action.id}"
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
