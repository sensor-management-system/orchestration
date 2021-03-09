import json

from project import base_url
from project.tests.base import BaseTestCase
from project.tests.models.test_device_calibration_action_model import (
    add_device_calibration_action,
)


class TestDeviceCalibrationAction(BaseTestCase):
    """Tests for the DeviceCalibrationAction endpoints."""

    device_calibration_action_url = base_url + "/device-calibration-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "device_calibration_action"
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = (
        "/usr/src/app/project/tests/drafts/platforms_test_data.json"
    )

    def test_get_device_calibration_action(self):
        """Ensure the GET /device_calibration_action route reachable."""
        response = self.client.get(self.device_calibration_action_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_calibration_action_collection(self):
        """Test retrieve a collection of DeviceCalibrationAction objects"""
        uda = add_device_calibration_action()
        with self.client:
            response = self.client.get(self.device_calibration_action_url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(uda.description, data["data"][0]["attributes"]["description"])

    def test_post_device_calibration_action(self):
        """Create DeviceCalibrationAction"""

    def test_update_device_calibration_action(self):
        """Update DeviceCalibration"""
        dca = add_device_calibration_action()
        c_updated = {
            "data": {
                "type": self.object_type,
                "id": dca.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.device_calibration_action_url}/{dca.id}",
            data_object=c_updated,
            object_type=self.object_type,
        )

    def test_delete_device_calibration_action(self):
        """Delete DeviceCalibrationAction"""
        dca = add_device_calibration_action()
        _ = super().delete_object(
            url=f"{self.device_calibration_action_url}/{dca.id}",
        )
