import json

from project import base_url
from project.api.models import Contact, Device, Platform
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_unmount_actions_model import add_unmount_device_action


class TestDeviceUnmountAction(BaseTestCase):
    """Tests for the DeviceUnmountAction endpoints."""

    device_unmount_action_url = base_url + "/device-unmount-actions"
    object_type = "device_unmount_action"

    def test_get_device_unmount_action(self):
        """Ensure the GET /device_unmount_actions route reachable."""
        response = self.client.get(self.device_unmount_action_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_unmount_action_collection(self):
        """Test retrieve a collection of DeviceUnmountAction objects"""
        mpa = add_unmount_device_action()
        with self.client:
            response = self.client.get(self.device_unmount_action_url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            mpa.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            data["data"][0]["attributes"]["end_date"],
        )

    def test_post_device_unmount_action(self):
        """Create DeviceUnmountAction"""
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
                    "description": "test unmount device action",
                    "end_date": fake.future_datetime().__str__(),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": d.id}},
                    "contact": {"data": {"type": "contact", "id": c1.id}},
                    "configuration": {
                        "data": {"type": "configuration", "id": config.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.device_unmount_action_url}?include=device,contact,configuration",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_unmount_action(self):
        """Update DeviceUnmountAction"""
        mpa = add_unmount_device_action()
        mpa_updated = {
            "data": {
                "type": self.object_type,
                "id": mpa.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
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
