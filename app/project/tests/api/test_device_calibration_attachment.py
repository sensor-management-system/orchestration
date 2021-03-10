import json

from project import base_url
from project.tests.base import BaseTestCase
from project.tests.models.test_device_calibration_attachment_model import (
    add_device_calibration_attachment,
)


class TestDeviceCalibrationAttachment(BaseTestCase):
    """Tests for the DeviceCalibrationAttachment endpoints."""

    device_calibration_attachment_url = base_url + "/device-calibration-attachments"
    object_type = "device_calibration_attachment"

    def test_get_generic_device_action_attachment(self):
        """Ensure the GET /device_calibration_attachment route reachable."""
        response = self.client.get(self.device_calibration_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_calibration_action_attachment_collection(self):
        """Test retrieve a collection of DeviceCalibrationAttachment objects"""
        dca = add_device_calibration_attachment()
        response = self.client.get(self.device_calibration_attachment_url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            dca.attachment.id, data["data"][0]["attributes"]["attachment"].id
        )

    def test_post_generic_device_action_attachment(self):
        """Create DeviceCalibrationAttachment"""
        pass

    def test_update_generic_device_action_attachment(self):
        """Update DeviceCalibrationAttachment"""
        pass

    def test_delete_generic_device_action_attachment(self):
        """Delete DeviceCalibrationAttachment"""
        dca = add_device_calibration_attachment()
        _ = super().delete_object(
            url=f"{self.device_calibration_attachment_url}/{dca.id}",
        )
