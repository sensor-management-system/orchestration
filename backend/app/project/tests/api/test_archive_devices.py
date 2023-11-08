# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the archivation of devices."""

import datetime
from unittest.mock import patch

import pytz

from project import base_url
from project.api.models import Configuration, Contact, Device, DeviceMountAction, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.restframework.preconditions.devices import (
    AllMountsOfDeviceAreFinishedInThePast,
    AllUsagesAsParentDeviceInDeviceMountsFinishedInThePast,
)
from project.tests.base import BaseTestCase


class TestArchiveDevice(BaseTestCase):
    """Test class to archive devices."""

    devices_url = base_url + "/devices"

    def setUp(self):
        """Set up some data to test with."""
        super().setUp()

        self.public_device = Device(
            short_name="simple device",
            archived=False,
            is_public=True,
            is_private=False,
            is_internal=False,
            update_description="create;basic data",
        )
        self.internal_device = Device(
            short_name="also device",
            archived=False,
            is_public=False,
            is_private=False,
            is_internal=True,
            update_description="create;basic data",
        )
        self.private_device = Device(
            short_name="not so simple device",
            archived=False,
            is_public=False,
            is_private=True,
            is_internal=False,
            update_description="create;basic data",
        )
        contact1 = Contact(
            given_name="test", family_name="user", email="test.user@localhost"
        )
        contact2 = Contact(
            given_name="super", family_name="user", email="super.user@localhost"
        )
        self.normal_user = User(subject=contact1.email, contact=contact1)
        self.super_user = User(
            subject=contact2.email, contact=contact2, is_superuser=True
        )
        self.configuration = Configuration(
            label="Test configuration", is_public=True, is_internal=False
        )
        db.session.add_all(
            [
                self.public_device,
                self.internal_device,
                self.private_device,
                contact1,
                contact2,
                self.normal_user,
                self.super_user,
                self.configuration,
            ]
        )
        db.session.commit()

    def test_get(self):
        """Ensure that it is not allowed to use the get method."""
        response = self.client.get(f"{self.devices_url}/12345/archive")
        self.assertEqual(response.status_code, 405)

    def test_post_unauthorized(self):
        """Ensure that we don't allow anonymous to archive."""
        response = self.client.post(f"{self.devices_url}/12345/archive")
        self.assertEqual(response.status_code, 401)

    def test_post_nonexisting(self):
        """Ensure that we got an 404 when the device doesn't exist."""
        with self.run_requests_as(self.normal_user):
            response = self.client.post(f"{self.devices_url}/12345/archive")
        self.assertEqual(response.status_code, 404)

    def test_post_user_not_in_idl(self):
        """Ensure that an ordinary user without an entry in the idl can't archive."""
        self.public_device.group_ids = ["123"]
        db.session.add(self.public_device)
        db.session.commit()

        with patch.object(
            idl, "get_all_permission_groups_for_a_user", return_value=None
        ):
            with self.run_requests_as(self.normal_user):
                response = self.client.post(
                    f"{self.devices_url}/{self.public_device.id}/archive"
                )
            self.assertEqual(response.status_code, 403)

    def test_post_user_not_in_any_group(self):
        """Ensure that an ordinary user without group membership can't archive."""
        self.public_device.group_ids = ["123"]
        db.session.add(self.public_device)
        db.session.commit()

        with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
            mock.return_value = UserAccount(
                id="1000",
                username=self.normal_user.subject,
                administrated_permission_groups=[],
                membered_permission_groups=[],
            )
            with self.run_requests_as(self.normal_user):
                response = self.client.post(
                    f"{self.devices_url}/{self.public_device.id}/archive"
                )
            self.assertEqual(response.status_code, 403)

    def test_post_user_in_a_group(self):
        """Ensure that an ordinary user can't archive."""
        self.public_device.group_ids = ["123"]
        db.session.add(self.public_device)
        db.session.commit()

        with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
            mock.return_value = UserAccount(
                id="1000",
                username=self.normal_user.subject,
                administrated_permission_groups=[],
                membered_permission_groups=["123"],
            )
            with self.run_requests_as(self.normal_user):
                response = self.client.post(
                    f"{self.devices_url}/{self.public_device.id}/archive"
                )
            self.assertEqual(response.status_code, 403)

    def test_post_admin_in_a_group(self):
        """Ensure that we can set the archived flag as admins."""
        self.public_device.group_ids = ["123"]
        db.session.add(self.public_device)
        db.session.commit()

        with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
            mock.return_value = UserAccount(
                id="1000",
                username=self.normal_user.subject,
                administrated_permission_groups=["123"],
                membered_permission_groups=[],
            )
            with self.run_requests_as(self.normal_user):
                response = self.client.post(
                    f"{self.devices_url}/{self.public_device.id}/archive"
                )
        self.assertEqual(response.status_code, 204)
        reloaded_device = (
            db.session.query(Device).filter_by(id=self.public_device.id).one()
        )
        self.assertTrue(reloaded_device.archived)
        self.assertEqual(reloaded_device.update_description, "archive;basic data")
        self.assertEqual(reloaded_device.updated_by_id, self.normal_user.id)

    def test_post_superuser(self):
        """Ensure that we can set the archived flag super user."""
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.devices_url}/{self.public_device.id}/archive"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_device = (
            db.session.query(Device).filter_by(id=self.public_device.id).one()
        )
        self.assertTrue(reloaded_device.archived)
        self.assertEqual(reloaded_device.update_description, "archive;basic data")
        self.assertEqual(reloaded_device.updated_by_id, self.super_user.id)

    def test_post_already_archived(self):
        """Ensure that it doesn't matter if the device is already archived."""
        self.public_device.archived = True
        db.session.add(self.public_device)
        db.session.commit()

        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.devices_url}/{self.public_device.id}/archive"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_device = (
            db.session.query(Device).filter_by(id=self.public_device.id).one()
        )
        self.assertTrue(reloaded_device.archived)
        self.assertEqual(reloaded_device.update_description, "create;basic data")
        self.assertIsNone(reloaded_device.updated_by_id)

    def test_post_private_device_different_user(self):
        """Ensure that a user can't archive a private device of another user."""
        self.private_device.created_by_id = self.super_user.id
        db.session.add(self.private_device)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                f"{self.devices_url}/{self.private_device.id}/archive"
            )
        self.assertEqual(response.status_code, 403)

    def test_post_private_device_same_user(self):
        """Ensure that a user can archive a private device of her/himself."""
        self.private_device.created_by_id = self.normal_user.id
        db.session.add(self.private_device)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                f"{self.devices_url}/{self.private_device.id}/archive"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_device = (
            db.session.query(Device).filter_by(id=self.private_device.id).one()
        )
        self.assertTrue(reloaded_device.archived)
        self.assertEqual(reloaded_device.update_description, "archive;basic data")
        self.assertEqual(reloaded_device.updated_by_id, self.normal_user.id)

    def test_post_private_device_super_user(self):
        """Ensure that a super user can archive a private device of other users."""
        self.private_device.created_by_id = self.normal_user.id
        db.session.add(self.private_device)
        db.session.commit()
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.devices_url}/{self.private_device.id}/archive"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_device = (
            db.session.query(Device).filter_by(id=self.private_device.id).one()
        )
        self.assertTrue(reloaded_device.archived)
        self.assertEqual(reloaded_device.update_description, "archive;basic data")
        self.assertEqual(reloaded_device.updated_by_id, self.super_user.id)

    def test_post_device_super_user_conflict_due_to_device_mount_without_end(self):
        """Ensure that we can't archive a device if there is a device mount without end."""
        device_mount_action = DeviceMountAction(
            device=self.public_device,
            configuration=self.configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(device_mount_action)
        db.session.commit()
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.devices_url}/{self.public_device.id}/archive"
            )
        self.assertEqual(response.status_code, 409)

    def test_post_device_super_user_conflict_due_to_device_mount_end_in_the_future(
        self,
    ):
        """Ensure that we can't archive a device if there is a device mount end in the future."""
        device_mount_action = DeviceMountAction(
            device=self.public_device,
            configuration=self.configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2012, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
            end_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(device_mount_action)
        db.session.commit()
        with patch.object(
            AllMountsOfDeviceAreFinishedInThePast, "_get_current_date_time"
        ) as mock:
            mock.return_value = datetime.datetime(2022, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
            with self.run_requests_as(self.super_user):
                response = self.client.post(
                    f"{self.devices_url}/{self.public_device.id}/archive"
                )
        self.assertEqual(response.status_code, 409)

    def test_post_device_super_user_conflict_due_to_parent_device_mount_without_end(
        self,
    ):
        """Ensure we can't archive a device if a parent device mount has no end."""
        parent_mount_action = DeviceMountAction(
            device=self.internal_device,
            parent_device=self.public_device,
            configuration=self.configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(parent_mount_action)
        db.session.commit()
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.devices_url}/{self.public_device.id}/archive"
            )
        self.assertEqual(response.status_code, 409)

    def test_post_device_super_user_conflict_due_to_parent_device_mount_end_in_the_future(
        self,
    ):
        """Ensure we can't archive devices if a parent device mount ends in the future."""
        parent_mount_action = DeviceMountAction(
            device=self.internal_device,
            parent_device=self.public_device,
            configuration=self.configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2012, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
            end_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(parent_mount_action)
        db.session.commit()
        with patch.object(
            AllUsagesAsParentDeviceInDeviceMountsFinishedInThePast,
            "_get_current_date_time",
        ) as mock:
            mock.return_value = datetime.datetime(2022, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
            with self.run_requests_as(self.super_user):
                response = self.client.post(
                    f"{self.devices_url}/{self.public_device.id}/archive"
                )
        self.assertEqual(response.status_code, 409)
