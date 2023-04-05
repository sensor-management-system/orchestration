# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Test classes for the device property calibrations."""
import datetime
import json
from unittest.mock import patch

import pytz

from project import base_url
from project.api.models import (
    Contact,
    Device,
    DeviceCalibrationAction,
    DeviceProperty,
    DevicePropertyCalibration,
    User,
)
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase


class TestDevicePropertyCalibrations(BaseTestCase):
    """Test class for the device property calibrations."""

    url = base_url + "/device-property-calibrations"

    def test_patch_to_non_editable_device(self):
        """Ensure we can't update to a device we can't edit."""
        device1 = Device(
            short_name="device1",
            is_public=False,
            is_internal=True,
            is_private=False,
            group_ids=["1"],
        )
        device2 = Device(
            short_name="device2",
            is_public=False,
            is_internal=True,
            is_private=False,
            group_ids=["2"],
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        action1 = DeviceCalibrationAction(
            device=device1,
            contact=contact,
            current_calibration_date=datetime.datetime(
                2022, 12, 24, 0, 0, 0, tzinfo=pytz.utc
            ),
        )
        action2 = DeviceCalibrationAction(
            device=device2,
            contact=contact,
            current_calibration_date=datetime.datetime(
                2022, 12, 24, 0, 0, 0, tzinfo=pytz.utc
            ),
        )
        device_property1 = DeviceProperty(
            device=device1,
            property_uri="https://gfz-potsdam.de",
            property_name="temp",
        )
        device_property2 = DeviceProperty(
            device=device2,
            property_uri="https://ufz.de",
            property_name="humidity",
        )
        device_property_calibration = DevicePropertyCalibration(
            calibration_action=action1,
            device_property=device_property1,
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all(
            [
                device1,
                device2,
                contact,
                user,
                action1,
                action2,
                device_property1,
                device_property2,
                device_property_calibration,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "device_property_calibration",
                "id": device_property_calibration.id,
                "attributes": {},
                "relationships": {
                    # We try to switch here to another device for
                    # which we have no edit permissions.
                    "device_property": {
                        "data": {
                            "type": "device_property",
                            "id": device_property2.id,
                        }
                    },
                    "calibration_action": {
                        "data": {
                            "type": "device_calibration_action",
                            "id": action2.id,
                        }
                    },
                },
            }
        }

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[*device1.group_ids],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.url}/{device_property_calibration.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)
