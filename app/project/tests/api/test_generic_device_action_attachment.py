from project import base_url
from project.tests.base import BaseTestCase


class TestGenericDeviceActionAttachment(BaseTestCase):
    """Tests for the GenericDeviceActionAttachment endpoints."""

    generic_device_action_attachment_url = base_url + "/generic-device-action-attachments"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "generic_device_action"
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = (
        "/usr/src/app/project/tests/drafts/platforms_test_data.json"
    )

    def test_get_generic_device_action_attachment(self):
        """Ensure the GET /generic_device_action_attachments route reachable."""
        response = self.client.get(self.generic_device_action_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_device_action_attachment_collection(self):
        """Test retrieve a collection of GenericDeviceActionAttachment objects"""
        pass

    def test_post_generic_device_action_attachment(self):
        """Create GenericDeviceActionAttachment"""
        pass

    def test_update_generic_device_action_attachment(self):
        """Update GenericDeviceActionAttachment"""
        pass

    def test_delete_generic_device_action_attachment(self):
        """Delete GenericDeviceActionAttachment """
        pass
