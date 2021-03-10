from project import base_url
from project.tests.base import BaseTestCase

from project.tests.models.test_software_update_actions_attachment_model import \
    add_platform_software_update_action_attachment_model


class TestPlatformSoftwareUpdateActionAttachment(BaseTestCase):
    """Tests for the PlatformSoftwareUpdateActionAttachment endpoints."""

    platform_software_update_action_attachment_url = (
            base_url + "/platform-software-update-action-attachments"
    )
    object_type = "platform_software_update_action_attachment"

    def test_get_platform_software_update_action_attachment(self):
        """Ensure the GET /platform_software_update_action_attachments route reachable."""
        response = self.client.get(self.platform_software_update_action_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_platform_software_update_action_attachment_collection(self):
        """Test retrieve a collection of PlatformSoftwareUpdateActionAttachment objects"""
        _ = add_platform_software_update_action_attachment_model()
        response = self.client.get(self.platform_software_update_action_attachment_url)
        self.assertEqual(response.status_code, 200)

    def test_post_platform_software_update_action_attachment(self):
        """Create PlatformSoftwareUpdateActionAttachment"""
        pass

    def test_update_platform_software_update_action_attachment(self):
        """Update PlatformSoftwareUpdateActionAttachment"""
        pass

    def test_delete_platform_software_update_action_attachment(self):
        """Delete PlatformSoftwareUpdateActionAttachment """
        psu_a = add_platform_software_update_action_attachment_model()
        _ = super().delete_object(
            url=f"{self.platform_software_update_action_attachment_url}/{psu_a.id}",
        )
