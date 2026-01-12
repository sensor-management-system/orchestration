# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Test classes for the device property calibrations."""
import datetime
import json

from project import base_url
from project.api.models import (
    Contact,
    Device,
    DeviceCalibrationAction,
    DeviceProperty,
    DevicePropertyCalibration,
    PermissionGroup,
    PermissionGroupMembership,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestDevicePropertyCalibrations(BaseTestCase):
    """Test class for the device property calibrations."""

    url = base_url + "/device-property-calibrations"

    def setUp(self):
        """Set stuff up for the tests."""
        super().setUp()
        normal_contact = Contact(
            given_name="normal", family_name="user", email="normal.user@localhost"
        )
        self.normal_user = User(subject=normal_contact.email, contact=normal_contact)

        self.permission_group = PermissionGroup(name="test", entitlement="test")
        self.other_group = PermissionGroup(name="other", entitlement="other")
        self.membership = PermissionGroupMembership(
            permission_group=self.permission_group, user=self.normal_user
        )
        db.session.add_all(
            [
                normal_contact,
                self.normal_user,
                self.permission_group,
                self.other_group,
                self.membership,
            ]
        )
        db.session.commit()

    def test_patch_to_non_editable_device(self):
        """Ensure we can't update to a device we can't edit."""
        device1 = Device(
            short_name="device1",
            is_public=False,
            is_internal=True,
            is_private=False,
            group_ids=[self.permission_group.id],
        )
        device2 = Device(
            short_name="device2",
            is_public=False,
            is_internal=True,
            is_private=False,
            group_ids=[self.other_group.id],
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
                2022, 12, 24, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
        )
        action2 = DeviceCalibrationAction(
            device=device2,
            contact=contact,
            current_calibration_date=datetime.datetime(
                2022, 12, 24, 0, 0, 0, tzinfo=datetime.timezone.utc
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
        db.session.add_all(
            [
                device1,
                device2,
                contact,
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

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.url}/{device_property_calibration.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)
