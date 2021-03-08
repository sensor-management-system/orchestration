from project import base_url
from project.tests.base import BaseTestCase


class TestGenericPlatformActionAttachment(BaseTestCase):
    """Tests for the GenericPlatformActionAttachment endpoints."""

    generic_platform_action_attachment_url = base_url + "/generic-platform-action-attachments"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "generic_device_action"
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = (
        "/usr/src/app/project/tests/drafts/platforms_test_data.json"
    )

    def test_get_generic_platform_action_attachment(self):
        """Ensure the GET /generic_platform_action_attachments route reachable."""
        response = self.client.get(self.generic_platform_action_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_platform_action_attachment_collection(self):
        """Test retrieve a collection of GenericPlatformActionAttachment objects"""
        pass

    def test_post_generic_platform_action_attachment(self):
        """Create GenericPlatformActionAttachment"""
        pass

    def test_update_generic_platform_action_attachment(self):
        """Update GenericPlatformActionAttachment"""
        pass

    def test_delete_generic_platform_action_attachment(self):
        """Delete GenericPlatformActionAttachment """
        pass
