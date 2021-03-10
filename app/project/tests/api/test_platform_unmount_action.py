import json

from project import base_url
from project.tests.base import BaseTestCase
from project.tests.models.test_unmount_actions_model import add_unmount_platform_action


class TestPlatformUnmountAction(BaseTestCase):
    """Tests for the PlatformUnmountAction endpoints."""

    platform_unmount_action_url = base_url + "/platform-unmount-actions"
    object_type = "platform_unmount_action"

    def test_get_platform_unmount_action(self):
        """Ensure the GET /platform_unmount_actions route reachable."""
        response = self.client.get(self.platform_unmount_action_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_platform_unmount_action_collection(self):
        """Test retrieve a collection of PlatformUnmountAction objects"""
        uda = add_unmount_platform_action()
        response = self.client.get(self.platform_unmount_action_url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(uda.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                         data["data"][0]["attributes"]["end_date"])

    def test_post_platform_unmount_action(self):
        """Create PlatformUnmountAction"""
        pass

    def test_update_platform_unmount_action(self):
        """Update PlatformUnmountAction"""
        upa = add_unmount_platform_action()
        c_updated = {
            "data": {
                "type": self.object_type,
                "id": upa.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.platform_unmount_action_url}/{upa.id}",
            data_object=c_updated,
            object_type=self.object_type,
        )

    def test_delete_platform_unmount_action(self):
        """Delete PlatformUnmountAction """
        upa = add_unmount_platform_action()
        _ = super().delete_object(
            url=f"{self.platform_unmount_action_url}/{upa.id}",
        )
