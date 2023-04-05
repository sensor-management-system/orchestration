# SPDX-FileCopyrightText: 2021
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.schemas.device_schema import DeviceSchema
from project.tests.base import BaseTestCase


class TestDeviceModel(BaseTestCase):
    """Tests for the Device Model."""

    def test_add_device_model(self):
        """""Ensure Add device model """
        sensor = Device(
            id=22,
            short_name="device_short_name test",
            description="device_description test",
            long_name="device_long_name test",
            manufacturer_name="manufacturer_name test",
            manufacturer_uri="http://cv/manufacturer_uri",
            model="device_model test",
            dual_use=True,
            serial_number="device_serial_number test",
            website="http://website/device",
            inventory_number="inventory_number test",
            persistent_identifier="persistent_identifier_test",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        DeviceSchema().dump(sensor)
        db.session.add(sensor)
        db.session.commit()

        device = db.session.query(Device).filter_by(id=sensor.id).one()
        self.assertIn(device.model, sensor.model)
