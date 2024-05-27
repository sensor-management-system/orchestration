# SPDX-FileCopyrightText: 2021 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the device model."""

from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.schemas.device_schema import DeviceSchema
from project.tests.base import BaseTestCase


class TestDeviceModel(BaseTestCase):
    """Tests for the device model."""

    def test_add_device_model(self):
        """Ensure that we can add a device model to the database."""
        sensor = Device(
            id=22,
            short_name="device_short_name test",
            description="device_description test",
            long_name="device_long_name test",
            manufacturer_name="manufacturer_name test",
            manufacturer_uri="http://cv/manufacturer_uri",
            model="device_model test",
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

    def test_text_search_fields(self):
        """Ensure the most important fields are in the fields for full text search."""
        text_fields = Device.text_search_fields()
        self.assertTrue("short_name" in text_fields)
        self.assertFalse("created_by_id" in text_fields)
