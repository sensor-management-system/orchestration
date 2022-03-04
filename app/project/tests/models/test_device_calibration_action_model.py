from project.api.models import (
    Contact,
    Device,
    DeviceCalibrationAction,
    DeviceProperty,
    DevicePropertyCalibration,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data


def add_device_calibration_action():
    device = Device(short_name="Device 12",
                    is_public=False,
                    is_private=False,
                    is_internal=True,
                    )
    device = Device(short_name="Device 12")
    userinfo = generate_userinfo_data()
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
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
    return device_calibration_action


def add_device_property_calibration_model():
    device = Device(short_name="Device 20",
                    is_public=False,
                    is_private=False,
                    is_internal=True,
                    )
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
    userinfo = generate_userinfo_data()
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
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
    dpc = DevicePropertyCalibration(
        device_property=device_property, calibration_action=device_calibration_action
    )
    db.session.add_all(
        [device_property, device, contact, device_calibration_action, dpc]
    )
    db.session.commit()
    return dpc


class TestDeviceCalibrationActionModel(BaseTestCase):
    """Tests for the DeviceCalibrationAction & DevicePropertyCalibration Models."""

    def test_device_calibration_action(self):
        """""Ensure Add device calibration action  model """
        device_calibration_action = add_device_calibration_action()
        self.assertTrue(device_calibration_action.id is not None)

    def test_add_device_property_calibration(self):
        """""Ensure Add device property calibration model."""
        device_property_calibration_model = add_device_property_calibration_model()
        self.assertTrue(device_property_calibration_model.id is not None)
