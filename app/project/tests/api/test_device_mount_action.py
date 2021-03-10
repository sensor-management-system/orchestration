import json

from project import base_url
from project.api.models import Contact, Device, Platform
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_mount_actions_model import add_mount_device_action_model


class TestDeviceMountAction(BaseTestCase):
    """Tests for the DeviceMountAction endpoints."""

    device_mount_action_url = base_url + "/device-mount-actions"
    object_type = "device_mount_action"

    def test_get_device_mount_action(self):
        """Ensure the GET /device_mount_actions route reachable."""
        response = self.client.get(self.device_mount_action_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_mount_action_collection(self):
        """Test retrieve a collection of DeviceMountAction objects"""
        dma = add_mount_device_action_model()
        with self.client:
            response = self.client.get(self.device_mount_action_url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dma.description, data["data"][0]["attributes"]["description"])

    def test_post_device_mount_action(self):
        """Create DeviceMountAction"""
        d = Device(
            short_name=fake.linux_processor(),
        )
        p_p = Platform(
            short_name="device parent platform",
        )
        jwt1 = generate_token_data()
        c1 = Contact(
            given_name=jwt1["given_name"],
            family_name=jwt1["family_name"],
            email=jwt1["email"],
        )
        config = generate_configuration_model()
        db.session.add_all([d, p_p, c1, config])
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
                    "device": {"data": {"type": "device", "id": d.id}},
                    "contact": {"data": {"type": "contact", "id": c1.id}},
                    "parent_platform": {"data": {"type": "platform", "id": p_p.id}},
                    "configuration": {
                        "data": {"type": "configuration", "id": config.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.device_mount_action_url}?include=device,contact,parent_platform,configuration",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_mount_action(self):
        """Update DeviceMountAction"""
        dma = add_mount_device_action_model()
        c_updated = {
            "data": {
                "type": self.object_type,
                "id": dma.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.device_mount_action_url}/{dma.id}",
            data_object=c_updated,
            object_type=self.object_type,
        )

    def test_delete_device_mount_action(self):
        """Delete DeviceMountAction """
        dma = add_mount_device_action_model()
        _ = super().delete_object(
            url=f"{self.device_mount_action_url}/{dma.id}",
        )
