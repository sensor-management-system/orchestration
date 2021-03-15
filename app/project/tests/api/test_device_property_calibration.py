from project import base_url
from project.api.models import Contact, Device, DeviceCalibrationAction, DeviceProperty
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_device_calibration_action_model import (
    add_device_property_calibration_model,
)


class TestDevicePropertyCalibration(BaseTestCase):
    """Tests for the DevicePropertyCalibration endpoints."""

    url = base_url + "/device-property-calibrations"
    object_type = "device_property_calibration"

    def test_get_device_property_calibration(self):
        """Ensure the GET /device_property_calibration route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_property_calibration_collection(self):
        """Test retrieve a collection of DevicePropertyCalibration objects"""
        device_property_calibration_model = add_device_property_calibration_model()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # should be only one
        self.assertEqual(response.json["meta"]["count"], 1)
        self.assertEqual(
            response.json["data"][0]["id"], str(device_property_calibration_model.id)
        )

    def test_post_device_property_calibration(self):
        """Create DevicePropertyCalibration"""
        device = Device(short_name="Device 200")
        device_property = DeviceProperty(
            device=device,
            measuring_range_min=fake.pyfloat(),
            measuring_range_max=fake.pyfloat(),
            failure_value=fake.pyfloat(),
            accuracy=fake.pyfloat(),
            label=fake.pystr(),
            unit_uri=fake.uri(),
            unit_name=fake.pystr(),
            compartment_uri=fake.uri(),
            compartment_name=fake.pystr(),
            property_uri=fake.uri(),
            property_name="Test property_name",
            sampling_media_uri=fake.uri(),
            sampling_media_name=fake.pystr(),
        )
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        device_calibration_action = DeviceCalibrationAction(
            description="Test DeviceCalibrationAction",
            formula=fake.pystr(),
            value=fake.pyfloat(),
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            device=device,
            contact=contact,
        )
        db.session.add_all(
            [device, contact, device_property, device_calibration_action]
        )
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "device_property": {
                        "data": {"type": "device_property", "id": device_property.id}
                    },
                    "calibration_action": {
                        "data": {
                            "type": "device_calibration_action",
                            "id": device_calibration_action.id,
                        }
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=device_property,calibration_action",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_property_calibration(self):
        """Update DevicePropertyCalibration"""
        device = Device(short_name="Device 300")
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )

        device_calibration_action = DeviceCalibrationAction(
            description="Test DeviceCalibrationAction",
            formula=fake.pystr(),
            value=fake.pyfloat(),
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            device=device,
            contact=contact,
        )
        db.session.add_all([device, contact, device_calibration_action])
        db.session.commit()
        dpa = add_device_property_calibration_model()
        data = {
            "data": {
                "type": self.object_type,
                "id": dpa.id,
                "attributes": {},
                "relationships": {
                    "calibration_action": {
                        "data": {
                            "type": "device_calibration_action",
                            "id": device_calibration_action.id,
                        }
                    },
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{dpa.id}?include=calibration_action",
            data_object=data,
            object_type=self.object_type,
        )

    def test_delete_device_property_calibration(self):
        """Delete DevicePropertyCalibration """
        device_property_calibration = add_device_property_calibration_model()
        _ = super().delete_object(
            url=f"{self.url}/{device_property_calibration.id}",
        )
