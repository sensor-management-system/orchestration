import json

from project import base_url
from project.api.models import Contact, Device
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_software_update_actions_model import (
    add_device_software_update_action_model,
)


class TestDeviceSoftwareUpdateAction(BaseTestCase):
    """Tests for the DeviceSoftwareUpdateAction endpoints."""

    url = base_url + "/device-software-update-actions"
    object_type = "device_software_update_action"

    def test_get_device_software_update_action(self):
        """Ensure the GET /device_software_update_action route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_software_update_action_collection(self):
        """Test retrieve a collection of DeviceSoftwareUpdateAction objects"""
        sau = add_device_software_update_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sau.description, data["data"][0]["attributes"]["description"])

    def test_post_device_software_update_action(self):
        """Create DeviceSoftwareUpdateAction"""
        device = Device(short_name="Device 1")
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        db.session.add_all([device, contact])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "Test DeviceCalibrationAction",
                    "version": f"v_{fake.pyint()}",
                    "software_type_name": fake.pystr(),
                    "software_type_uri": fake.uri(),
                    "repository_url": fake.url(),
                    "update_date": fake.future_datetime().__str__(),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=device,contact",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_software_update_action(self):
        """Update DeviceSoftwareUpdateAction"""
        device_software_update_action = add_device_software_update_action_model()
        device_software_update_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_software_update_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{device_software_update_action.id}",
            data_object=device_software_update_action_updated,
            object_type=self.object_type,
        )

    def test_delete_device_software_update_action(self):
        """Delete DeviceSoftwareUpdateAction"""
        device_software_update_action = add_device_software_update_action_model()
        _ = super().delete_object(
            url=f"{self.url}/{device_software_update_action.id}",
        )
