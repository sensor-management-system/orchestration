import json

from project import base_url
from project.api.models import Contact, Device, Platform
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_mount_actions_model import add_mount_device_action_model


class TestDeviceMountAction(BaseTestCase):
    """Tests for the DeviceMountAction endpoints."""

    url = base_url + "/device-mount-actions"
    object_type = "device_mount_action"

    def test_get_device_mount_action(self):
        """Ensure the GET /device_mount_actions route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_mount_action_collection(self):
        """Test retrieve a collection of DeviceMountAction objects"""
        mount_device_action = add_mount_device_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            mount_device_action.description,
            data["data"][0]["attributes"]["description"],
        )

    def test_post_device_mount_action(self):
        """Create DeviceMountAction"""
        device = Device(
            short_name=fake.linux_processor(),
        )
        parent_platform = Platform(
            short_name="device parent platform",
        )
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        configuration = generate_configuration_model()
        db.session.add_all([device, parent_platform, contact, configuration])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "Test DeviceMountAction",
                    "begin_date": fake.future_datetime().__str__(),
                    "offset_x": str(fake.coordinate()),
                    "offset_y": str(fake.coordinate()),
                    "offset_z": str(fake.coordinate()),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "parent_platform": {
                        "data": {"type": "platform", "id": parent_platform.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=device,contact,parent_platform,configuration",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_mount_action(self):
        """Update DeviceMountAction"""
        mount_device_action = add_mount_device_action_model()
        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_device_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{mount_device_action.id}",
            data_object=mount_device_action_updated,
            object_type=self.object_type,
        )

    def test_delete_device_mount_action(self):
        """Delete DeviceMountAction """
        mount_device_action = add_mount_device_action_model()
        _ = super().delete_object(
            url=f"{self.url}/{mount_device_action.id}",
        )
