from project import base_url
from project.tests.base import BaseTestCase

from project.tests.models.test_software_update_actions_model import \
    add_platform_software_update_action_model


class TestPlatformSoftwareUpdateAction(BaseTestCase):
    """Tests for the PlatformSoftwareUpdateAction endpoints."""

    platform_software_update_action_url = base_url + "/platform-software-update-actions"
    object_type = "platform_software_update_action"

    def test_get_platform_software_update_action(self):
        """Ensure the GET /platform_software_update_actions route reachable."""
        response = self.client.get(self.platform_software_update_action_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_platform_software_update_action_collection(self):
        """Test retrieve a collection of PlatformSoftwareUpdateAction objects"""
        _ = add_platform_software_update_action_model()
        response = self.client.get(self.platform_software_update_action_url)
        self.assertEqual(response.status_code, 200)

    def test_post_platform_software_update_action(self):
        """Create PlatformSoftwareUpdateAction"""
        pass

    def test_update_platform_software_update_action(self):
        """Update PlatformSoftwareUpdateAction"""

    def test_delete_platform_software_update_action(self):
        """Delete PlatformSoftwareUpdateAction """
        psu = add_platform_software_update_action_model()
        _ = super().delete_object(
            url=f"{self.platform_software_update_action_url}/{psu.id}",
        )
