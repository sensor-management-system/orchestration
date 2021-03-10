from project import base_url
from project.tests.base import BaseTestCase


class TestDeviceSoftwareUpdateAction(BaseTestCase):
    """Tests for the DeviceSoftwareUpdateAction endpoints."""

    device_software_update_action_url = base_url + "/device-software-update-actions"
    object_type = "device_software_update_action"

    def test_get_device_software_update_action(self):
        """Ensure the GET /device_software_update_action route reachable."""
        response = self.client.get(self.device_software_update_action_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_software_update_action_collection(self):
        """Test retrieve a collection of DeviceSoftwareUpdateAction objects"""

    def test_post_device_software_update_action(self):
        """Create DeviceSoftwareUpdateAction"""

    def test_update_device_software_update_action(self):
        """Update DeviceSoftwareUpdateAction"""

    def test_delete_device_software_update_action(self):
        """Delete DeviceSoftwareUpdateAction"""
