# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

from project.api.models import (
    Contact,
    Device,
    DeviceCalibrationAction,
    DeviceProperty,
    DevicePropertyCalibration,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data


def add_device_calibration_action(
    public=True, private=False, internal=False, group_ids=None
):
    if group_ids is None:
        group_ids = []
    device = Device(
        short_name="Device 12",
        manufacturer_name=fake.company(),
        is_public=public,
        is_private=private,
        is_internal=internal,
        group_ids=group_ids,
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
    db.session.add_all([device, contact, device_calibration_action])
    db.session.commit()
    return device_calibration_action


def add_device_property_calibration_model():
    device = Device(
        short_name="Device 20",
        manufacturer_name=fake.company(),
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
