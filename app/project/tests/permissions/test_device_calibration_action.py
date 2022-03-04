"""Tests for the device calibration api."""

import json

from project import base_url
from project.tests.base import BaseTestCase
from project.tests.base import create_token
from project.tests.models.test_device_calibration_action_model import (
    add_device_calibration_action,
)


class TestDeviceCalibrationAction(BaseTestCase):
    """Tests for the DeviceCalibrationAction endpoints."""

    url = base_url + "/device-calibration-actions"
    object_type = "device_calibration_action"

    def test_get_public_device_calibration_action(self):
        """Test retrieve a collection of DeviceCalibrationAction objects."""
        device_calibration_action = add_device_calibration_action()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            device_calibration_action.description,
            data["data"][0]["attributes"]["description"],
        )

    def test_get_internal_device_calibration_action(self):
        """Test retrieve a collection of internal DeviceCalibrationAction objects."""
        _ = add_device_calibration_action(public=False, private=False, internal=True)
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
