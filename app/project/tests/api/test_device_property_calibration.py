from project import base_url
from project.tests.base import BaseTestCase
from project.tests.models.test_device_calibration_action_model import (
    add_device_property_calibration_model,
)


class TestDevicePropertyCalibration(BaseTestCase):
    """Tests for the DevicePropertyCalibration endpoints."""

    device_property_calibration_url = base_url + "/device-property-calibrations"
    object_type = "device_property_calibration"

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
        dpa = add_device_property_calibration_model()
        _ = super().delete_object(
            url=f"{self.device_property_calibration_url}/{dpa.id}",
        )
