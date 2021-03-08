from project.api.models import (Contact, DeviceCalibrationAction, DevicePropertyCalibration,
                                DeviceProperty, Device, Platform)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.base import fake
from project.tests.base import generate_token_data


class TestDeviceCalibrationActionModel(BaseTestCase):
    """Tests for the DeviceCalibrationAction & DevicePropertyCalibration Models."""

    def test_device_calibration_action(self):
        """""Ensure Add device calibration action  model """
        d = Device(short_name="Device 12")
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
        db.session.add_all([d, c, dca])
        db.session.commit()
        self.assertTrue(dca.id is not None)

    def test_add_device_property_calibration(self):
        """""Ensure Add device property calibration model."""
        d = Device(short_name="Device 20")
        dp = DeviceProperty(
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
            sampling_media_name=fake.pystr(), )
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

        dpc = DevicePropertyCalibration(device_property=dp)
        db.session.add_all([dp, d, c, dca, dpc])
        db.session.commit()
        self.assertTrue(dpc.id is not None)
