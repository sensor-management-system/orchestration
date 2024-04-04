# SPDX-FileCopyrightText: 2020 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Test cases for the csv export functionality."""

import io
from csv import DictReader

from project import base_url
from project.api.models import Device, Platform, DeviceProperty
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestDeviceCsvExport(BaseTestCase):
    """Test case for the csv export for devices."""

    device_url = base_url + "/devices"

    def test_csv_response(self):
        """Ensure the csv export for devices works."""
        sensor1 = Device(
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
        db.session.add(sensor1)
        db.session.commit()
        sensor2 = Device(
            id=33,
            short_name="device_short_name test2",
            description="device_description test2",
            long_name="device_long_name test2",
            manufacturer_name="manufacturer_name test2",
            manufacturer_uri="http://cv/manufacturer_uri2",
            model="device_model test2",
            serial_number="device_serial_number test2",
            website="http://website/device2",
            inventory_number="inventory_number test2",
            persistent_identifier="persistent_identifier_test2",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(sensor2)

        # Make the object public.
        sensor1.is_internal = False
        sensor2.is_internal = False
        sensor1.is_public = True
        sensor2.is_public = True

        db.session.commit()
        response = self.client.get(
            self.device_url,
            headers={"Content-Type": "application/vnd.api+json", "Accept": "text/csv"},
        )
        # still need to be converted to dict WIP
        rows = list(DictReader(response.data.decode().split("\n")))
        # Since we only have sensor1 and sensor2, there should be just 2 rows
        assert len(rows) == 2
        # The names should be in the dictionary
        names = set([row["short_name"] for row in rows])
        assert "device_short_name test" in names
        assert "device_short_name test2" in names

    def test_cleanup_newlines(self):
        """Test the csv export with multiline descriptions."""
        sensor1 = Device(
            id=22,
            short_name="device_short_name test",
            description="Line1\n\nLine2\n\n\nLine3",
            long_name="device_long_name test",
            manufacturer_name="manufacturer_name test",
            manufacturer_uri="http://cv/manufacturer_uri",
            model="device_model test",
            serial_number="device_serial_number test",
            website="http://website/device",
            inventory_number="inventory_number test",
            persistent_identifier="persistent_identifier_test",
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        db.session.add(sensor1)
        db.session.commit()
        response = self.client.get(
            self.device_url,
            headers={"Content-Type": "application/vnd.api+json", "Accept": "text/csv"},
        )
        dict_reader = DictReader(io.StringIO(response.text))
        rows = list(dict_reader)
        assert len(rows) == 1
        # As it cause trouble when opening on windows (and opening in excel)
        # we don't export mulitlines.
        # Instead we replace them with spaces.
        # The text will still be readable, but it looses a little bit
        # of structure.
        self.assertEqual(rows[0]["description"], "Line1 Line2 Line3")

    def test_includes_device_proeprties(self):
        """Ensure that we can include the device properties."""
        device1 = Device(
            id=22,
            short_name="device_short_name test",
            description="some description",
            long_name="device_long_name test",
            manufacturer_name="manufacturer_name test",
            manufacturer_uri="http://cv/manufacturer_uri",
            model="device_model test",
            serial_number="device_serial_number test",
            website="http://website/device",
            inventory_number="inventory_number test",
            persistent_identifier="persistent_identifier_test",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device_property1 = DeviceProperty(
            device=device1,
            label="dp1",
            property_name = "Air Temperature"
        )
        device_property2 = DeviceProperty(
            device=device1,
            label="dp2",
            property_name = "Humidity"
        )

        db.session.add_all([device1, device_property1, device_property2])
        db.session.commit()
        response = self.client.get(
            self.device_url,
            headers={"Content-Type": "application/vnd.api+json", "Accept": "text/csv"},
        )
        dict_reader = DictReader(io.StringIO(response.text))
        rows = list(dict_reader)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertIn("properties_0_label", row.keys())
        self.assertEqual(row["properties_0_label"], device_property1.label)
        self.assertIn("properties_1_label", row.keys())
        self.assertEqual(row["properties_1_label"], device_property2.label)


class TestPlatformCsvExport(BaseTestCase):
    """Test class for the csv export for platforms."""

    platform_url = base_url + "/platforms"

    def test_csv_response(self):
        """Ensure csv export for platforms works."""
        platform1 = Platform(
            id=22,
            short_name="platform_short_name test",
            description="platform_description test",
            long_name="platform_long_name test",
            manufacturer_name="manufacturer_name test",
            manufacturer_uri="http://cv/manufacturer_uri",
            model="platform_model test",
            serial_number="platform_serial_number test",
            website="http://website/platform",
            inventory_number="inventory_number test",
            persistent_identifier="persistent_identifier_test",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(platform1)
        db.session.commit()
        platform2 = Platform(
            id=33,
            short_name="platform_short_name test2",
            description="platform_description test2",
            long_name="platform_long_name test2",
            manufacturer_name="manufacturer_name test2",
            manufacturer_uri="http://cv/manufacturer_uri2",
            model="platform_model test2",
            serial_number="platform_serial_number test2",
            website="http://website/platform2",
            inventory_number="inventory_number test2",
            persistent_identifier="persistent_identifier_test2",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(platform2)

        # Make the object public.
        platform1.is_internal = False
        platform2.is_internal = False
        platform1.is_public = True
        platform2.is_public = True

        db.session.commit()
        response = self.client.get(
            self.platform_url,
            headers={"Content-Type": "application/vnd.api+json", "Accept": "text/csv"},
        )
        # still need to be converted to dict WIP
        rows = list(DictReader(response.data.decode().split("\n")))
        # Since we only have platform1 and platform2, there should be just 2 rows
        assert len(rows) == 2
        # The names should be in the dictionary
        names = set([row["short_name"] for row in rows])
        assert "platform_short_name test" in names
        assert "platform_short_name test2" in names
