"""Tests for the custom field endpoints."""

import json
from unittest.mock import patch

from project import base_url
from project.api.models.base_model import db
from project.api.models.customfield import CustomField
from project.api.models.device import Device
from project.api.services.idl_services import Idl
from project.tests.base import BaseTestCase, create_token, query_result_to_list
from project.tests.base import fake
from project.tests.permissions import create_a_test_device
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def prepare_custom_field_payload(device):
    payload = {
        "data": {
            "type": "customfield",
            "attributes": {"value": fake.pystr(), "key": fake.pystr(),},
            "relationships": {
                "device": {"data": {"type": "device", "id": str(device.id)}}
            },
        }
    }
    return payload


class TestCustomFieldServices(BaseTestCase):
    """Test customfields."""

    url = base_url + "/customfields"

    def test_get_public_customfields(self):
        """Ensure that we can get a list of public customfields."""
        device1 = Device(
            short_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device2 = Device(
            short_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        customfield1 = CustomField(
            key="GFZ", value="https://www.gfz-potsdam.de", device=device1,
        )
        customfield2 = CustomField(
            key="UFZ", value="https://www.ufz.de", device=device1,
        )
        customfield3 = CustomField(
            key="PIK", value="https://www.pik-potsdam.de", device=device2,
        )

        db.session.add(customfield1)
        db.session.add(customfield2)
        db.session.add(customfield3)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url + "/customfields", content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

    def test_get_internal_customfields(self):
        """Ensure that we can get a list of internal customfields only with a valid jwt."""
        device1 = Device(
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        device2 = Device(
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        customfield1 = CustomField(
            key="GFZ", value="https://www.gfz-potsdam.de", device=device1,
        )
        customfield2 = CustomField(
            key="UFZ", value="https://www.ufz.de", device=device1,
        )

        db.session.add(customfield1)
        db.session.add(customfield2)
        db.session.commit()

        with self.client:
            response = self.client.get(
                self.url, content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

    def test_post_to_a_device_with_a_permission_group(self):
        """Post to device,with permission Group."""
        device = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(device.id is not None)
        count_customfields = (
            db.session.query(CustomField).filter_by(device_id=device.id,).count()
        )

        self.assertEqual(count_customfields, 0)
        payload = prepare_custom_field_payload(device)
        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url_post = base_url + "/customfields"

                response = self.client.post(
                    url_post,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

        self.assertEqual(response.status_code, 201)
        customfields = query_result_to_list(
            db.session.query(CustomField).filter_by(device_id=device.id,)
        )
        self.assertEqual(len(customfields), 1)

        customfield = customfields[0]
        self.assertEqual(customfield.value, payload["data"]["attributes"]["value"])
        self.assertEqual(customfield.key, payload["data"]["attributes"]["key"])
        self.assertEqual(customfield.device_id, device.id)
        self.assertEqual(str(customfield.device_id), response.get_json()["data"]["id"])

    def test_post_to_a_device_with_an_other_permission_group(self):
        """Post to a device with a different permission Group from the user."""
        device = create_a_test_device([66])
        self.assertTrue(device.id is not None)
        count_customfields = (
            db.session.query(CustomField).filter_by(device_id=device.id,).count()
        )

        self.assertEqual(count_customfields, 0)
        payload = prepare_custom_field_payload(device)
        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url_post = base_url + "/customfields"

                response = self.client.post(
                    url_post,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

        self.assertEqual(response.status_code, 403)

    def test_patch_to_a_device_with_a_permission_group(self):
        """Patch Custom field attached to device with same group as user."""
        device = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(device.id is not None)
        count_customfields = (
            db.session.query(CustomField).filter_by(device_id=device.id,).count()
        )

        self.assertEqual(count_customfields, 0)
        customfield = CustomField(
            key="GFZ", value="https://www.gfz-potsdam.de", device=device,
        )
        db.session.add(customfield)
        db.session.commit()
        payload = {
            "data": {
                "id": customfield.id,
                "type": "customfield",
                "attributes": {"value": "changed", "key": customfield.key},
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = base_url + "/customfields/" + str(customfield.id)

                response = self.client.patch(
                    url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(customfield.value, data["data"]["attributes"]["value"])
        self.assertEqual(customfield.key, data["data"]["attributes"]["key"])
        self.assertEqual(customfield.device_id, device.id)

    def test_delete_to_a_device_with_a_permission_group(self):
        """Delete Custom field attached to device with same group as user
        (user is admin)."""
        device = create_a_test_device(IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertTrue(device.id is not None)
        count_customfields = (
            db.session.query(CustomField).filter_by(device_id=device.id,).count()
        )

        self.assertEqual(count_customfields, 0)
        customfield = CustomField(
            key="GFZ", value="https://www.gfz-potsdam.de", device=device,
        )
        db.session.add(customfield)
        db.session.commit()
        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = base_url + "/customfields/" + str(customfield.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

    def test_delete_to_a_device_with_a_permission_group_as_a_member(self):
        """Delete Custom field attached to device with same group as user
                (user is member)."""
        device = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(device.id is not None)
        count_customfields = (
            db.session.query(CustomField).filter_by(device_id=device.id,).count()
        )

        self.assertEqual(count_customfields, 0)
        customfield = CustomField(
            key="GFZ", value="https://www.gfz-potsdam.de", device=device,
        )
        db.session.add(customfield)
        db.session.commit()
        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = base_url + "/customfields/" + str(customfield.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)
