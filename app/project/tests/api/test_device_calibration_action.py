import json

from project import base_url
from project.api.models import Contact, Device
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_device_calibration_action_model import (
    add_device_calibration_action,
)


class TestDeviceCalibrationAction(BaseTestCase):
    """Tests for the DeviceCalibrationAction endpoints."""

    url = base_url + "/device-calibration-actions"
    object_type = "device_calibration_action"

    def test_get_device_calibration_action(self):
        """Ensure the GET /device_calibration_action route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_calibration_action_collection(self):
        """Test retrieve a collection of DeviceCalibrationAction objects"""
        device_calibration_action = add_device_calibration_action()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            device_calibration_action.description,
            data["data"][0]["attributes"]["description"],
        )

    def test_post_device_calibration_action(self):
        """Create DeviceCalibrationAction"""
        device = Device(short_name="Device 12")
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
                    "formula": fake.pystr(),
                    "value": fake.pyfloat(),
                    "current_calibration_date": fake.future_datetime().__str__(),
                    "next_calibration_date": fake.future_datetime().__str__(),
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

    def test_update_device_calibration_action(self):
        """Update DeviceCalibration"""
        device_calibration_action = add_device_calibration_action()
        device_calibration_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_calibration_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{device_calibration_action.id}",
            data_object=device_calibration_action_updated,
            object_type=self.object_type,
        )

    def test_delete_device_calibration_action(self):
        """Delete DeviceCalibrationAction"""
        device_calibration_action = add_device_calibration_action()
        _ = super().delete_object(
            url=f"{self.url}/{device_calibration_action.id}",
        )
