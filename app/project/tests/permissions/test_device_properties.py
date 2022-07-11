"""Tests for the device property endpoints."""

import json
from unittest.mock import patch

from project import base_url
from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.models.device_property import DeviceProperty
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list
from project.tests.permissions.test_customfields import create_a_test_device
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def device_properties_model(public=True, private=False, internal=False, group_ids=None):
    device1 = Device(
        short_name=fake.pystr(),
        manufacturer_name=fake.company(),
        is_public=public,
        is_private=private,
        is_internal=internal,
        group_ids=group_ids,
    )
    device2 = Device(
        short_name=fake.pystr(),
        manufacturer_name=fake.company(),
        is_public=public,
        is_private=private,
        is_internal=internal,
        group_ids=group_ids,
    )
    db.session.add(device1)
    db.session.add(device2)
    db.session.commit()
    device_property1 = DeviceProperty(
        label="device property1", property_name="device_property1", device=device1,
    )
    device_property2 = DeviceProperty(
        label="device property2", property_name="device_property2", device=device1,
    )
    device_property3 = DeviceProperty(
        label="device property3", property_name="device_property3", device=device2,
    )
    db.session.add_all([device_property1, device_property2, device_property3])
    db.session.commit()
    return device1, device2, device_property1, device_property2, device_property3


class TestDevicePropertyServices(BaseTestCase):
    """Test device properties."""

    url = base_url + "/device-properties"

    def test_get_public_device_property_api(self):
        """Ensure that we can get a list of public device properties."""
        _ = device_properties_model()

        with self.client:
            response = self.client.get(
                self.url,
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

    def test_get_internal_device_property_api(self):
        """Ensure that we can get a list of internal device properties with a valid jwt."""
        _ = device_properties_model(public=False, private=False, internal=True)

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
            self.assertEqual(len(response.json["data"]), 3)

    def test_post_device_property_api(self):
        """Ensure that we can add a device property."""
        device = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(device.id is not None)

        count_device_properties = (
            db.session.query(DeviceProperty)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )
        self.assertEqual(count_device_properties, 0)
        payload = {
            "data": {
                "type": "device_property",
                "attributes": {
                    "label": "device property1",
                    "property_name": "device_property1",
                    "compartment_name": "climate",
                    "sampling_media_name": "air",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
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
        device_properties = query_result_to_list(
            db.session.query(DeviceProperty).filter_by(
                device_id=device.id,
            )
        )
        self.assertEqual(len(device_properties), 1)

        device_property = device_properties[0]
        self.assertEqual(device_property.label, "device property1")
        self.assertEqual(device_property.compartment_name, "climate")
        self.assertEqual(device_property.sampling_media_name, "air")
        self.assertEqual(device_property.device_id, device.id)
        self.assertEqual(
            str(device_property.device_id), response.get_json()["data"]["id"]
        )

    def test_patch_device_property_api(self):
        """Ensure that we can update a device property."""
        device1 = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
        device2 = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)

        device_property1 = DeviceProperty(
            label="property 1", property_name="device_property1", device=device1,
        )
        db.session.add(device_property1)
        db.session.commit()

        payload = {
            "data": {
                "type": "device_property",
                "id": str(device_property1.id),
                "attributes": {
                    "label": "property 2",
                    "property_name": "device_property2",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device2.id)}}
                },
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url_patch = base_url + "/device-properties/" + str(device_property1.id)
                response = self.client.patch(
                    url_patch,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

        self.assertEqual(response.status_code, 200)

        device_property_reloaded = (
            db.session.query(DeviceProperty).filter_by(id=device_property1.id).one()
        )
        self.assertEqual(device_property_reloaded.label, "property 2")
        self.assertEqual(device_property_reloaded.device_id, device2.id)

    def test_delete_device_property_api(self):
        """Ensure that we can delete a device property."""
        device = Device(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
            group_ids=IDL_USER_ACCOUNT.administrated_permission_groups,
        )
        device_property = DeviceProperty(
            label="device property1", property_name="device_property1", device=device,
        )
        db.session.add_all([device, device_property])
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    self.url + "/" + str(device_property.id),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

            self.assertEqual(response.status_code, 200)
