from project import base_url
from project.tests.base import BaseTestCase


class TestPlatformSoftwareUpdateActionAttachment(BaseTestCase):
    """Tests for the PlatformSoftwareUpdateActionAttachment endpoints."""

    platform_software_update_action_attachment_url = (
        base_url + "/platform-software-update-action-attachments"
    )
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "generic_device_action"
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = (
        "/usr/src/app/project/tests/drafts/platforms_test_data.json"
    )

    def test_get_platform_software_update_action_attachment(self):
        """Ensure the GET /platform_software_update_action_attachments route reachable."""
        response = self.client.get(self.platform_software_update_action_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_platform_software_update_action_attachment_collection(self):
        """Test retrieve a collection of PlatformSoftwareUpdateActionAttachment objects"""

    def test_post_platform_software_update_action_attachment(self):
        """Create PlatformSoftwareUpdateActionAttachment"""

    def test_update_platform_software_update_action_attachment(self):
        """Update PlatformSoftwareUpdateActionAttachment"""

    def test_delete_platform_software_update_action_attachment(self):
        """Delete PlatformSoftwareUpdateActionAttachment """
