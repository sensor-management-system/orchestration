from project import base_url
from project.tests.base import BaseTestCase
from project.tests.models.test_generic_action_attachment_model import (
    add_generic_platform_action_attachment_model,
)


class TestGenericPlatformActionAttachment(BaseTestCase):
    """Tests for the GenericPlatformActionAttachment endpoints."""

    generic_platform_action_attachment_url = (
        base_url + "/generic-platform-action-attachments"
    )
    object_type = "generic_platform_action_attachment"

    def test_get_generic_platform_action_attachment(self):
        """Ensure the GET /generic_platform_action_attachments route reachable."""
        response = self.client.get(self.generic_platform_action_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_platform_action_attachment_collection(self):
        """Test retrieve a collection of GenericPlatformActionAttachment objects"""
        _ = add_generic_platform_action_attachment_model()
        with self.client:
            response = self.client.get(self.generic_platform_action_attachment_url)
        self.assertEqual(response.status_code, 200)

    def test_post_generic_platform_action_attachment(self):
        """Create GenericPlatformActionAttachment"""

    def test_update_generic_platform_action_attachment(self):
        """Update GenericPlatformActionAttachment"""

    def test_delete_generic_platform_action_attachment(self):
        """Delete GenericPlatformActionAttachment """
        dpa_a = add_generic_platform_action_attachment_model()
        _ = super().delete_object(
            url=f"{self.generic_platform_action_attachment_url}/{dpa_a.id}",
        )
