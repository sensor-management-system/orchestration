import json

from project import base_url
from project.tests.base import BaseTestCase
from project.tests.models.test_mount_actions_model import add_mount_device_action_model


class TestDeviceMountAction(BaseTestCase):
    """Tests for the DeviceMountAction endpoints."""

    device_mount_action_url = base_url + "/device-mount-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "device_mount_action"
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
        dma = add_mount_device_action_model()
        with self.client:
            response = self.client.get(self.device_mount_action_url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dma.description, data["data"][0]["attributes"]["description"])

    def test_post_device_mount_action(self):
        """Create DeviceMountAction"""

    def test_update_device_mount_action(self):
        """Update DeviceMountAction"""
        dma = add_mount_device_action_model()
        c_updated = {
            "data": {
                "type": self.object_type,
                "id": dma.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.device_mount_action_url}/{dma.id}",
            data_object=c_updated,
            object_type=self.object_type,
        )

    def test_delete_device_mount_action(self):
        """Delete DeviceMountAction """
        dma = add_mount_device_action_model()
        _ = super().delete_object(
            url=f"{self.device_mount_action_url}/{dma.id}",
        )
