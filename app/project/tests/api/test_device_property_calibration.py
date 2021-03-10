from project import base_url
from project.api.models import Device, DeviceProperty, Contact, DeviceCalibrationAction
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.base import fake
from project.tests.base import generate_token_data
from project.tests.models.test_device_calibration_action_model import (
    add_device_property_calibration_model,
)


class TestDevicePropertyCalibration(BaseTestCase):
    """Tests for the DevicePropertyCalibration endpoints."""

    device_property_calibration_url = base_url + "/device-property-calibrations"
    object_type = "device_property_calibration"

    def test_get_device_property_calibration(self):
        """Ensure the GET /device_property_calibration route reachable."""
        response = self.client.get(self.device_property_calibration_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_property_calibration_collection(self):
        """Test retrieve a collection of DevicePropertyCalibration objects"""
        _ = add_device_property_calibration_model
        response = self.client.get(self.device_property_calibration_url)
        self.assertEqual(response.status_code, 200)

    def test_post_device_property_calibration(self):
        """Create DevicePropertyCalibration"""
        d = Device(short_name="Device 200")
        dp = DeviceProperty(
            device=d,
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
        jwt1 = generate_token_data()
        c = Contact(
            given_name=jwt1["given_name"],
            family_name=jwt1["family_name"],
            email=jwt1["email"],
        )
        dca = DeviceCalibrationAction(
            description="Test DeviceCalibrationAction",
            formula=fake.pystr(),
            value=fake.pyfloat(),
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            device=d,
            contact=c,
        )
        db.session.add_all([d, c, dp, dca])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "device_property": {"data": {"type": "device_property", "id": dp.id}},
                    "calibration_action": {
                        "data": {"type": "device_calibration_action", "id": dca.id}},
                },
            }
        }
        _ = super().add_object(
            url=f"{self.device_property_calibration_url}?include=device_property,calibration_action",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_property_calibration(self):
        """Update DevicePropertyCalibration"""
        d = Device(short_name="Device 300")
        jwt1 = generate_token_data()
        c = Contact(
            given_name=jwt1["given_name"],
            family_name=jwt1["family_name"],
            email=jwt1["email"],
        )

        dca_neu = DeviceCalibrationAction(
            description="Test DeviceCalibrationAction",
            formula=fake.pystr(),
            value=fake.pyfloat(),
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            device=d,
            contact=c,
        )
        db.session.add_all([d, c, dca_neu])
        db.session.commit()
        dpa = add_device_property_calibration_model()
        data = {
            "data": {
                "type": self.object_type,
                "id": dpa.id,
                "attributes": {},
                "relationships": {
                    "calibration_action": {
                        "data": {"type": "device_calibration_action", "id": dca_neu.id}},
                },
            }
        }
        _ = super().update_object(
            url=f"{self.device_property_calibration_url}/{dpa.id}?include=calibration_action",
            data_object=data,
            object_type=self.object_type,
        )

    def test_delete_device_property_calibration(self):
        """Delete DevicePropertyCalibration """
        dpa = add_device_property_calibration_model()
        _ = super().delete_object(
            url=f"{self.device_property_calibration_url}/{dpa.id}",
        )
