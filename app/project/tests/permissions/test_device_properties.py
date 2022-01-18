"""Tests for the device property endpoints."""

import json

from project import base_url
from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.models.device_property import DeviceProperty
from project.tests.base import BaseTestCase, create_token, query_result_to_list


def device_properties_model(public=True, private=False, internal=False):
    device1 = Device(
        short_name="Just a device",
        is_public=public,
        is_private=private,
        is_internal=internal,
    )
    device2 = Device(
        short_name="Another device",
        is_public=public,
        is_private=private,
        is_internal=internal,
    )
    db.session.add(device1)
    db.session.add(device2)
    db.session.commit()
    device_property1 = DeviceProperty(label="device property1", device=device1, )
    device_property2 = DeviceProperty(label="device property2", device=device1, )
    device_property3 = DeviceProperty(label="device property3", device=device2, )
    db.session.add(device_property1)
    db.session.add(device_property2)
    db.session.add(device_property3)
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