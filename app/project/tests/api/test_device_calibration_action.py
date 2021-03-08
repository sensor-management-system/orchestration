from project import base_url
from project.tests.base import BaseTestCase


class TestDeviceCalibrationAction(BaseTestCase):
    """Tests for the DeviceCalibrationAction endpoints."""

    device_calibration_action_url = base_url + "/device-calibration-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "generic_device_action"
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = (
        "/usr/src/app/project/tests/drafts/platforms_test_data.json"
    )

    def test_get_generic_device_action(self):
        """Ensure the GET /device_calibration_action route reachable."""
        response = self.client.get(self.device_calibration_action_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_calibration_action_collection(self):
        """Test retrieve a collection of DeviceCalibrationAction objects"""
        pass

    def test_post_generic_device_action(self):
        """Create DeviceCalibrationAction"""
        pass

    def test_update_generic_device_action(self):
        """Update DeviceCalibration"""
        pass

    def test_delete_generic_device_action(self):
        """Delete DeviceCalibrationAction"""
        pass
