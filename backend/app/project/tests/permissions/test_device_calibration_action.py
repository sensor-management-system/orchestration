# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the device calibration api."""

import datetime
import json
from unittest.mock import patch

import pytz

from project import base_url
from project.api.models import Contact, Device, DeviceCalibrationAction, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake, generate_userinfo_data
from project.tests.models.test_device_calibration_action_model import (
    add_device_calibration_action,
)
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def add_device_and_contact(group_ids):
    """Add a device & a contact to the database & return them as tuple."""
    userinfo = generate_userinfo_data()
    device = Device(
        short_name=fake.pystr(),
        manufacturer_name=fake.company(),
        is_public=False,
        is_private=False,
        is_internal=True,
        group_ids=group_ids,
    )
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    db.session.add_all([device, contact])
    db.session.commit()

    return device, contact


def prepare_calibration_payload(object_type, group_ids):
    """Create some example payload to create calibration actions."""
    device, contact = add_device_and_contact(group_ids)
    data = {
        "data": {
            "type": object_type,
            "attributes": {
                "description": "Test DeviceCalibrationAction",
                "formula": fake.pystr(),
                "value": fake.pyfloat(),
                "current_calibration_date": fake.future_datetime().__str__(),
                "next_calibration_date": fake.future_datetime().__str__(),
            },
            "relationships": {
                "device": {"data": {"type": "device", "id": device.id}},
                "contact": {"data": {"type": "contact", "id": contact.id}},
            },
        }
    }
    return data


class TestDeviceCalibrationAction(BaseTestCase):
    """Tests for the DeviceCalibrationAction endpoints."""

    url = base_url + "/device-calibration-actions"
    object_type = "device_calibration_action"

    def test_get_public_device_calibration_action(self):
        """Test retrieve a collection of DeviceCalibrationAction objects."""
        device_calibration_action = add_device_calibration_action()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            device_calibration_action.description,
            data["data"][0]["attributes"]["description"],
        )

    def test_get_internal_device_calibration_action(self):
        """Test retrieve a collection of internal DeviceCalibrationAction objects."""
        _ = add_device_calibration_action(public=False, private=False, internal=True)
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_post_device_calibration_action_with_a_group(self):
        """Create DeviceCalibrationAction."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        data = prepare_calibration_payload(
            self.object_type, group_id_test_user_is_member_in_2
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,contact",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
        self.assertEqual(response.status_code, 201)

    def test_post_device_calibration_action_for_archived_device(self):
        """Create DeviceCalibrationAction."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        data = prepare_calibration_payload(
            self.object_type, group_id_test_user_is_member_in_2
        )
        device = db.session.query(Device).order_by("created_at").first()
        device.archived = True
        db.session.add(device)
        db.session.commit()
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,contact",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
        self.assertEqual(response.status_code, 403)

    def test_update_device_calibration_action(self):
        """Update DeviceCalibration."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device, contact = add_device_and_contact(group_id_test_user_is_member_in_2)
        device_calibration_action = DeviceCalibrationAction(
            description=fake.pystr(),
            formula=fake.pystr(),
            value=fake.pyfloat(),
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            device=device,
            contact=contact,
        )
        db.session.add(device_calibration_action)
        db.session.commit()
        device_calibration_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_calibration_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = f"{self.url}/{device_calibration_action.id}"

                response = self.client.patch(
                    url,
                    data=json.dumps(device_calibration_action_updated),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            device_calibration_action.description,
            data["data"]["attributes"]["description"],
        )
        self.assertEqual(device_calibration_action.device_id, device.id)

    def test_update_device_calibration_action_for_archived_device(self):
        """Ensure we can't update a device calibration action for archived devices."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device, contact = add_device_and_contact(group_id_test_user_is_member_in_2)
        device.archived = True
        device_calibration_action = DeviceCalibrationAction(
            description=fake.pystr(),
            formula=fake.pystr(),
            value=fake.pyfloat(),
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            device=device,
            contact=contact,
        )
        db.session.add_all([device_calibration_action, device])
        db.session.commit()
        device_calibration_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_calibration_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = f"{self.url}/{device_calibration_action.id}"

                response = self.client.patch(
                    url,
                    data=json.dumps(device_calibration_action_updated),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

        self.assertEqual(response.status_code, 403)

    def test_delete_device_calibration_action(self):
        """Delete DeviceCalibrationAction should succeed as a admin."""
        group_id_test_user_is_member_in_2 = (
            IDL_USER_ACCOUNT.administrated_permission_groups
        )
        device, contact = add_device_and_contact(group_id_test_user_is_member_in_2)
        device_calibration_action = DeviceCalibrationAction(
            description=fake.pystr(),
            formula=fake.pystr(),
            value=fake.pyfloat(),
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            device=device,
            contact=contact,
        )
        db.session.add(device_calibration_action)
        db.session.commit()
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    f"{self.url}/{device_calibration_action.id}",
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 200)

    def test_delete_device_calibration_action_for_archived_devices(self):
        """Ensure that we can't update calibrations for archived devices."""
        group_id_test_user_is_member_in_2 = (
            IDL_USER_ACCOUNT.administrated_permission_groups
        )
        device, contact = add_device_and_contact(group_id_test_user_is_member_in_2)
        device.archived = True
        device_calibration_action = DeviceCalibrationAction(
            description=fake.pystr(),
            formula=fake.pystr(),
            value=fake.pyfloat(),
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            device=device,
            contact=contact,
        )
        db.session.add_all([device_calibration_action, device])
        db.session.commit()
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    f"{self.url}/{device_calibration_action.id}",
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 403)

    def test_delete_device_calibration_action_as_member(self):
        """Delete DeviceCalibrationAction."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device, contact = add_device_and_contact(group_id_test_user_is_member_in_2)
        device_calibration_action = DeviceCalibrationAction(
            description=fake.pystr(),
            formula=fake.pystr(),
            value=fake.pyfloat(),
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            device=device,
            contact=contact,
        )
        db.session.add(device_calibration_action)
        db.session.commit()
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    f"{self.url}/{device_calibration_action.id}",
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 200)

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
        action = DeviceCalibrationAction(
            device=device1,
            contact=contact,
            current_calibration_date=datetime.datetime(
                2022, 12, 24, 0, 0, 0, tzinfo=pytz.utc
            ),
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all([device1, device2, contact, user, action])
        db.session.commit()

        payload = {
            "data": {
                "type": "device_calibration_action",
                "id": action.id,
                "attributes": {},
                "relationships": {
                    # We try to switch here to another device for
                    # which we have no edit permissions.
                    "device": {
                        "data": {
                            "type": "device",
                            "id": device2.id,
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
                        f"{self.url}/{action.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)
