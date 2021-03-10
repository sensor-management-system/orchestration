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

    device_calibration_action_url = base_url + "/device-calibration-actions"
    object_type = "device_calibration_action"

    def test_get_device_calibration_action(self):
        """Ensure the GET /device_calibration_action route reachable."""
        response = self.client.get(self.device_calibration_action_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_calibration_action_collection(self):
        """Test retrieve a collection of DeviceCalibrationAction objects"""
        uda = add_device_calibration_action()
        with self.client:
            response = self.client.get(self.device_calibration_action_url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(uda.description, data["data"][0]["attributes"]["description"])

    def test_post_device_calibration_action(self):
        """Create DeviceCalibrationAction"""
        d = Device(short_name="Device 12")
        jwt1 = generate_token_data()
        c = Contact(
            given_name=jwt1["given_name"],
            family_name=jwt1["family_name"],
            email=jwt1["email"],
        )
        db.session.add_all([d, c])
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
                    "device": {"data": {"type": "device", "id": d.id}},
                    "contact": {"data": {"type": "contact", "id": c.id}},
                },
            }
        }
        _ = super().add_object(
            url=f"{self.device_calibration_action_url}?include=device,contact",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_calibration_action(self):
        """Update DeviceCalibration"""
        dca = add_device_calibration_action()
        c_updated = {
            "data": {
                "type": self.object_type,
                "id": dca.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.device_calibration_action_url}/{dca.id}",
            data_object=c_updated,
            object_type=self.object_type,
        )

    def test_delete_device_calibration_action(self):
        """Delete DeviceCalibrationAction"""
        dca = add_device_calibration_action()
        _ = super().delete_object(
            url=f"{self.device_calibration_action_url}/{dca.id}",
        )
