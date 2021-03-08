import json

from project import base_url
from project.tests.base import BaseTestCase
from project.tests.models.test_unmount_actions_model import add_unmount_device_action


class TestDeviceUnmountAction(BaseTestCase):
    """Tests for the DeviceUnmountAction endpoints."""

    device_unmount_action_url = base_url + "/device-unmount-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "generic_device_action"
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = (
        "/usr/src/app/project/tests/drafts/platforms_test_data.json"
    )

    def test_get_device_unmount_action(self):
        """Ensure the GET /device_unmount_actions route reachable."""
        response = self.client.get(self.device_unmount_action_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_unmount_action_collection(self):
        """Test retrieve a collection of DeviceUnmountAction objects"""
        mpa = add_unmount_device_action()
        response = self.client.get(self.device_unmount_action_url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mpa.end_date, data["data"][0]["attributes"]["end_date"])

    def test_post_device_unmount_action(self):
        """Create DeviceUnmountAction"""
        pass

    def test_update_device_unmount_action(self):
        """Update DeviceUnmountAction"""
        mpa = add_unmount_device_action()
        mpa_updated = {
            "data": {"type": self.object_type, "id": mpa.id,
                     "attributes": {"given_name": "updated", }}}
        _ = super().update_object(
            url=f"{self.device_unmount_action_url}/{mpa.id}",
            data_object=mpa_updated,
            object_type=self.object_type,
        )

    def test_delete_device_unmount_action(self):
        """Delete DeviceUnmountAction """
        upa = add_unmount_device_action()
        _ = super().delete_object(
            url=f"{self.device_unmount_action_url}/{upa.id}",
        )
