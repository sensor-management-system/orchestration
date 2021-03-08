from project import base_url
from project.tests.base import BaseTestCase


class TestDevicePropertyCalibration(BaseTestCase):
    """Tests for the DevicePropertyCalibration endpoints."""

    device_property_calibration_url = base_url + "/device-property-calibrations"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "generic_device_action"
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = (
        "/usr/src/app/project/tests/drafts/platforms_test_data.json"
    )

    def test_get_device_property_calibration(self):
        """Ensure the GET /device_property_calibration route reachable."""
        response = self.client.get(self.device_property_calibration_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_property_calibration_collection(self):
        """Test retrieve a collection of DevicePropertyCalibration objects"""
        pass

    def test_post_device_property_calibration(self):
        """Create DevicePropertyCalibration"""
        pass

    def test_update_device_property_calibration(self):
        """Update DevicePropertyCalibration"""
        pass

    def test_delete_device_property_calibration(self):
        """Delete DevicePropertyCalibration """
        pass
