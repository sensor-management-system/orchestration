import json

from project import base_url
from project.api.models import Contact, Device
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_unmount_actions_model import add_unmount_device_action


class TestDeviceUnmountAction(BaseTestCase):
    """Tests for the DeviceUnmountAction endpoints."""

    url = base_url + "/device-unmount-actions"
    object_type = "device_unmount_action"

    def test_get_device_unmount_action(self):
        """Ensure the GET /device_unmount_actions route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_unmount_action_collection(self):
        """Test retrieve a collection of DeviceUnmountAction objects"""
        unmount_device_action = add_unmount_device_action()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            unmount_device_action.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            data["data"][0]["attributes"]["end_date"],
        )

    def test_post_device_unmount_action(self):
        """Create DeviceUnmountAction"""
        device = Device(
            short_name=fake.linux_processor(),
        )
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        configuration = generate_configuration_model()
        db.session.add_all([device, contact, configuration])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "test unmount device action",
                    "end_date": fake.future_datetime().__str__(),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=device,contact,configuration",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_unmount_action(self):
        """Update DeviceUnmountAction"""
        unmount_device_action = add_unmount_device_action()
        unmount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": unmount_device_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{unmount_device_action.id}",
            data_object=unmount_device_action_updated,
            object_type=self.object_type,
        )

    def test_delete_device_unmount_action(self):
        """Delete DeviceUnmountAction """
        unmount_device_action = add_unmount_device_action()
        _ = super().delete_object(
            url=f"{self.url}/{unmount_device_action.id}",
        )
