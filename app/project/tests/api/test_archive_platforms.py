# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the archivation of platforms."""

import datetime
from unittest.mock import patch

import pytz

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    Device,
    DeviceMountAction,
    Platform,
    PlatformMountAction,
    User,
)
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.restframework.preconditions.platforms import (
    AllMountsOfPlatformAreFinishedInThePast,
    AllUsagesAsParentPlatformInDeviceMountsFinishedInThePast,
    AllUsagesAsParentPlatformInPlatformMountsFinishedInThePast,
)
from project.tests.base import BaseTestCase


class TestArchivePlatform(BaseTestCase):
    """Test class to archive platforms."""

    platforms_url = base_url + "/platforms"

    def setUp(self):
        """Set up some data to test with."""
        super().setUp()

        self.public_platform = Platform(
            short_name="simple platform",
            archived=False,
            is_public=True,
            is_private=False,
            is_internal=False,
            update_description="create;basic data",
        )
        self.public_device = Device(
            short_name="simple device",
            archived=False,
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        self.internal_platform = Platform(
            short_name="also platform",
            archived=False,
            is_public=False,
            is_private=False,
            is_internal=True,
            update_description="create;basic data",
        )
        self.private_platform = Platform(
            short_name="not so simple platform",
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
                self.public_platform,
                self.internal_platform,
                self.public_device,
                self.private_platform,
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
        response = self.client.get(f"{self.platforms_url}/12345/archive")
        self.assertEqual(response.status_code, 405)

    def test_post_unauthorized(self):
        """Ensure that we don't allow anonymous to archive."""
        response = self.client.post(f"{self.platforms_url}/12345/archive")
        self.assertEqual(response.status_code, 401)

    def test_post_nonexisting(self):
        """Ensure that we got an 404 when the platform doesn't exist."""
        with self.run_requests_as(self.normal_user):
            response = self.client.post(f"{self.platforms_url}/12345/archive")
        self.assertEqual(response.status_code, 404)

    def test_post_user_not_in_idl(self):
        """Ensure that an ordinary user without an entry in the idl can't archive."""
        self.public_platform.group_ids = ["123"]
        db.session.add(self.public_platform)
        db.session.commit()

        with patch.object(
            idl, "get_all_permission_groups_for_a_user", return_value=None
        ):
            with self.run_requests_as(self.normal_user):
                response = self.client.post(
                    f"{self.platforms_url}/{self.public_platform.id}/archive"
                )
            self.assertEqual(response.status_code, 403)

    def test_post_user_not_in_any_group(self):
        """Ensure that an ordinary user without group membership can't archive."""
        self.public_platform.group_ids = ["123"]
        db.session.add(self.public_platform)
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
                    f"{self.platforms_url}/{self.public_platform.id}/archive"
                )
            self.assertEqual(response.status_code, 403)

    def test_post_user_in_a_group(self):
        """Ensure that an ordinary user can't archive."""
        self.public_platform.group_ids = ["123"]
        db.session.add(self.public_platform)
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
                    f"{self.platforms_url}/{self.public_platform.id}/archive"
                )
            self.assertEqual(response.status_code, 403)

    def test_post_admin_in_a_group(self):
        """Ensure that we can set the archived flag as admins."""
        self.public_platform.group_ids = ["123"]
        db.session.add(self.public_platform)
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
                    f"{self.platforms_url}/{self.public_platform.id}/archive"
                )
        self.assertEqual(response.status_code, 204)
        reloaded_platform = (
            db.session.query(Platform).filter_by(id=self.public_platform.id).one()
        )
        self.assertTrue(reloaded_platform.archived)
        self.assertEqual(reloaded_platform.update_description, "archive;basic data")
        self.assertEqual(reloaded_platform.updated_by_id, self.normal_user.id)

    def test_post_superuser(self):
        """Ensure that we can set the archived flag super user."""
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.public_platform.id}/archive"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_platform = (
            db.session.query(Platform).filter_by(id=self.public_platform.id).one()
        )
        self.assertTrue(reloaded_platform.archived)
        self.assertEqual(reloaded_platform.update_description, "archive;basic data")
        self.assertEqual(reloaded_platform.updated_by_id, self.super_user.id)

    def test_post_already_archived(self):
        """Ensure that it doesn't matter if the platform is already archived."""
        self.public_platform.archived = True
        db.session.add(self.public_platform)
        db.session.commit()

        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.public_platform.id}/archive"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_platform = (
            db.session.query(Platform).filter_by(id=self.public_platform.id).one()
        )
        self.assertTrue(reloaded_platform.archived)
        self.assertEqual(reloaded_platform.update_description, "create;basic data")
        self.assertIsNone(reloaded_platform.updated_by_id)

    def test_post_private_platform_different_user(self):
        """Ensure that a user can't archive a private platform of another user."""
        self.private_platform.created_by_id = self.super_user.id
        db.session.add(self.private_platform)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.private_platform.id}/archive"
            )
        self.assertEqual(response.status_code, 403)

    def test_post_private_platform_same_user(self):
        """Ensure that a user can archive a private platform of her/himself."""
        self.private_platform.created_by_id = self.normal_user.id
        db.session.add(self.private_platform)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.private_platform.id}/archive"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_platform = (
            db.session.query(Platform).filter_by(id=self.private_platform.id).one()
        )
        self.assertTrue(reloaded_platform.archived)
        self.assertEqual(reloaded_platform.update_description, "archive;basic data")
        self.assertEqual(reloaded_platform.updated_by_id, self.normal_user.id)

    def test_post_private_platform_super_user(self):
        """Ensure that a super user can archive a private platform of other users."""
        self.private_platform.created_by_id = self.normal_user.id
        db.session.add(self.private_platform)
        db.session.commit()
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.private_platform.id}/archive"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_platform = (
            db.session.query(Platform).filter_by(id=self.private_platform.id).one()
        )
        self.assertTrue(reloaded_platform.archived)
        self.assertEqual(reloaded_platform.update_description, "archive;basic data")
        self.assertEqual(reloaded_platform.updated_by_id, self.super_user.id)

    def test_post_platform_super_user_conflict_due_to_platform_mount_without_end(self):
        """Ensure that we can't archive a platform if there is a platform mount without end."""
        platform_mount_action = PlatformMountAction(
            platform=self.public_platform,
            configuration=self.configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(platform_mount_action)
        db.session.commit()
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.public_platform.id}/archive"
            )
        self.assertEqual(response.status_code, 409)

    def test_post_platform_super_user_conflict_due_to_platform_mount_end_in_the_future(
        self,
    ):
        """Ensure we can't archive platforms if a platform mount ends in the future."""
        platform_mount_action = PlatformMountAction(
            platform=self.public_platform,
            configuration=self.configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2012, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
            end_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(platform_mount_action)
        db.session.commit()
        with patch.object(
            AllMountsOfPlatformAreFinishedInThePast, "_get_current_date_time"
        ) as mock:
            mock.return_value = datetime.datetime(2022, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
            with self.run_requests_as(self.super_user):
                response = self.client.post(
                    f"{self.platforms_url}/{self.public_platform.id}/archive"
                )
        self.assertEqual(response.status_code, 409)

    def test_post_platform_super_user_conflict_due_to_parent_platform_mount_without_end(
        self,
    ):
        """Ensure we can't archive a platform if a parent platform mount has no end."""
        platform_mount_action = PlatformMountAction(
            platform=self.internal_platform,
            parent_platform=self.public_platform,
            configuration=self.configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(platform_mount_action)
        db.session.commit()
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.public_platform.id}/archive"
            )
        self.assertEqual(response.status_code, 409)

    def test_post_platform_super_user_conflict_due_to_parent_platform_mount_end_in_the_future(
        self,
    ):
        """Ensure we can't archive platforms if a parent platform mount ends in the future."""
        platform_mount_action = PlatformMountAction(
            platform=self.internal_platform,
            parent_platform=self.public_platform,
            configuration=self.configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2012, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
            end_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(platform_mount_action)
        db.session.commit()
        with patch.object(
            AllUsagesAsParentPlatformInPlatformMountsFinishedInThePast,
            "_get_current_date_time",
        ) as mock:
            mock.return_value = datetime.datetime(2022, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
            with self.run_requests_as(self.super_user):
                response = self.client.post(
                    f"{self.platforms_url}/{self.public_platform.id}/archive"
                )
        self.assertEqual(response.status_code, 409)

    def test_post_platform_super_user_conflict_due_to_parent_platform_device_mount_without_end(
        self,
    ):
        """Ensure we can't archive platforms if a parent platform device mount has no end."""
        device_mount_action = DeviceMountAction(
            device=self.public_device,
            parent_platform=self.public_platform,
            configuration=self.configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(device_mount_action)
        db.session.commit()
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.public_platform.id}/archive"
            )
        self.assertEqual(response.status_code, 409)

    def test_post_platform_super_user_conflict_parent_platform_device_mount_end_in_future(
        self,
    ):
        """Ensure we can't archive platforms if parent platform mount ends in the future."""
        device_mount_action = DeviceMountAction(
            device=self.public_device,
            parent_platform=self.public_platform,
            configuration=self.configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2012, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
            end_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(device_mount_action)
        db.session.commit()
        with patch.object(
            AllUsagesAsParentPlatformInDeviceMountsFinishedInThePast,
            "_get_current_date_time",
        ) as mock:
            mock.return_value = datetime.datetime(2022, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
            with self.run_requests_as(self.super_user):
                response = self.client.post(
                    f"{self.platforms_url}/{self.public_platform.id}/archive"
                )
        self.assertEqual(response.status_code, 409)
