# SPDX-FileCopyrightText: 2020 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

import io
from csv import DictReader

from project import base_url
from project.api.models.base_model import db
from project.api.models.device import Device
from project.tests.base import BaseTestCase


class Test(BaseTestCase):
    device_url = base_url + "/devices"

    def test_csv_response(self):
        """Ensure csv Export works"""
        super(Test, self).tearDown()
        super(Test, self).setUp()
        sensor1 = Device(
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
            dual_use=False,
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
        super(Test, self).tearDown()
        super(Test, self).setUp()
        sensor1 = Device(
            id=22,
            short_name="device_short_name test",
            description="Line1\n\nLine2\n\n\nLine3",
            long_name="device_long_name test",
            manufacturer_name="manufacturer_name test",
            manufacturer_uri="http://cv/manufacturer_uri",
            model="device_model test",
            dual_use=True,
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
