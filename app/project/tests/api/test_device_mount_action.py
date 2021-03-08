from project import base_url
from project.tests.base import BaseTestCase


class TestDeviceMountAction(BaseTestCase):
    """Tests for the DeviceMountAction endpoints."""

    device_mount_action_url = base_url + "/device-mount-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "generic_device_action"
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = (
        "/usr/src/app/project/tests/drafts/platforms_test_data.json"
    )

    def test_get_device_mount_action(self):
        """Ensure the GET /device_mount_actions route reachable."""
        response = self.client.get(self.device_mount_action_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_mount_action_collection(self):
        """Test retrieve a collection of DeviceMountAction objects"""
        pass

    def test_post_device_mount_action(self):
        """Create DeviceMountAction"""
        pass

    def test_update_device_mount_action(self):
        """Update DeviceMountAction"""
        pass

    def test_delete_device_mount_action(self):
        """Delete DeviceMountAction """
        pass
