from project import base_url
from project.tests.base import BaseTestCase

from project.tests.models.test_generic_action_attachment_model import \
    add_generic_device_action_attachment_model


class TestGenericDeviceActionAttachment(BaseTestCase):
    """Tests for the GenericDeviceActionAttachment endpoints."""

    generic_device_action_attachment_url = (
            base_url + "/generic-device-action-attachments"
    )
    object_type = "generic_device_action_attachment"

    def test_get_generic_device_action_attachment(self):
        """Ensure the GET /generic_device_action_attachments route reachable."""
        response = self.client.get(self.generic_device_action_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_device_action_attachment_collection(self):
        """Test retrieve a collection of GenericDeviceActionAttachment objects"""
        _ = add_generic_device_action_attachment_model()
        with self.client:
            response = self.client.get(self.generic_device_action_attachment_url)
        self.assertEqual(response.status_code, 200)

    def test_post_generic_device_action_attachment(self):
        """Create GenericDeviceActionAttachment"""
        pass

    def test_update_generic_device_action_attachment(self):
        """Update GenericDeviceActionAttachment"""
        pass

    def test_delete_generic_device_action_attachment(self):
        """Delete GenericDeviceActionAttachment """
        gda_a = add_generic_device_action_attachment_model()
        _ = super().delete_object(
            url=f"{self.generic_device_action_attachment_url}/{gda_a.id}",
        )
