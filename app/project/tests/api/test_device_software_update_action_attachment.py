import json

from project import base_url
from project.tests.base import BaseTestCase
from project.tests.models.test_software_update_actions_attachment_model import (
    add_device_software_update_action_attachment,
)


class TestDeviceSoftwareUpdateActionAttachment(BaseTestCase):
    """Tests for the DeviceSoftwareUpdateActionAttachment endpoints."""

    device_software_update_action_attachment_url = (
        base_url + "/device-software-update-action-attachments"
    )
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "device_software_update_action_attachment"
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = (
        "/usr/src/app/project/tests/drafts/platforms_test_data.json"
    )

    def test_get_device_software_update_action_attachment(self):
        """Ensure the GET /device_software_update_action_attachment route reachable."""
        response = self.client.get(self.device_software_update_action_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_software_update_action_attachment_collection(self):
        """Test retrieve a collection of DeviceSoftwareUpdateActionAttachment objects"""
        _ = add_device_software_update_action_attachment()
        with self.client:
            response = self.client.get(
                self.device_software_update_action_attachment_url
            )
        _ = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_post_device_software_update_action_attachment(self):
        """TEST Create DeviceSoftwareUpdateActionAttachment"""

    def test_update_device_software_update_action_attachment(self):
        """TEST Update DeviceSoftwareUpdateActionAttachment"""

    def test_delete_device_software_update_action_attachment(self):
        """TEST Delete DeviceSoftwareUpdateActionAttachment"""
        dsu = add_device_software_update_action_attachment()
        _ = super().delete_object(
            url=f"{self.device_software_update_action_attachment_url}/{dsu.id}",
        )
