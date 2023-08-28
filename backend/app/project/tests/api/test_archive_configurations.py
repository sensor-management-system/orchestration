# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the archivation of configurations."""

import datetime
from unittest.mock import patch

import pytz

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationDynamicLocationBeginAction,
    ConfigurationStaticLocationBeginAction,
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
from project.restframework.preconditions.configurations import (
    AllDeviceMountsForConfigurationAreFinishedInThePast,
    AllDynamicLocationsForConfigurationAreFinishedInThePast,
    AllPlatformMountsForConfigurationAreFinishedInThePast,
    AllStaticLocationsForConfigurationAreFinishedInThePast,
)
from project.tests.base import BaseTestCase


class TestArchiveConfiguration(BaseTestCase):
    """Test class to archive configurations."""

    configurations_url = base_url + "/configurations"

    def setUp(self):
        """Set up some data to test with."""
        super().setUp()

        self.public_device = Device(
            short_name="simple device",
            archived=False,
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        self.public_platform = Platform(
            short_name="simple platform",
            archived=False,
            is_public=True,
            is_private=False,
            is_internal=False,
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
        self.public_configuration = Configuration(
            label="Public configuration",
            is_public=True,
            is_internal=False,
            update_description="create;basic data",
        )

        db.session.add_all(
            [
                self.public_device,
                self.public_platform,
                contact1,
                contact2,
                self.normal_user,
                self.super_user,
                self.public_configuration,
            ]
        )
        db.session.commit()

    def test_get(self):
        """Ensure that it is not allowed to use the get method."""
        response = self.client.get(f"{self.configurations_url}/12345/archive")
        self.assertEqual(response.status_code, 405)

    def test_post_unauthorized(self):
        """Ensure that we don't allow anonymous to archive."""
        response = self.client.post(f"{self.configurations_url}/12345/archive")
        self.assertEqual(response.status_code, 401)

    def test_post_nonexisting(self):
        """Ensure that we got an 404 when the configuration doesn't exist."""
        with self.run_requests_as(self.normal_user):
            response = self.client.post(f"{self.configurations_url}/12345/archive")
        self.assertEqual(response.status_code, 404)

    def test_post_user_not_in_idl(self):
        """Ensure that an ordinary user without an entry in the idl can't archive."""
        self.public_configuration.cfg_permission_group = "123"
        db.session.add(self.public_configuration)
        db.session.commit()

        with patch.object(
            idl, "get_all_permission_groups_for_a_user", return_value=None
        ):
            with self.run_requests_as(self.normal_user):
                response = self.client.post(
                    f"{self.configurations_url}/{self.public_configuration.id}/archive"
                )
            self.assertEqual(response.status_code, 403)

    def test_post_user_not_in_any_group(self):
        """Ensure that an ordinary user without group membership can't archive."""
        self.public_configuration.cfg_permisison_group = "123"
        db.session.add(self.public_configuration)
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
                    f"{self.configurations_url}/{self.public_configuration.id}/archive"
                )
            self.assertEqual(response.status_code, 403)

    def test_post_user_in_a_group(self):
        """Ensure that an ordinary user can't archive."""
        self.public_configuration.cfg_perimssion_group = "123"
        db.session.add(self.public_configuration)
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
                    f"{self.configurations_url}/{self.public_configuration.id}/archive"
                )
            self.assertEqual(response.status_code, 403)

    def test_post_admin_in_a_group(self):
        """Ensure that we can set the archived flag as admins."""
        self.public_configuration.cfg_permission_group = "123"
        db.session.add(self.public_configuration)
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
                    f"{self.configurations_url}/{self.public_configuration.id}/archive"
                )
        self.assertEqual(response.status_code, 204)
        reloaded_configuration = (
            db.session.query(Configuration)
            .filter_by(id=self.public_configuration.id)
            .one()
        )
        self.assertTrue(reloaded_configuration.archived)
        self.assertEqual(
            reloaded_configuration.update_description, "archive;basic data"
        )
        self.assertEqual(reloaded_configuration.updated_by_id, self.normal_user.id)

    def test_post_superuser(self):
        """Ensure that we can set the archived flag super user."""
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.public_configuration.id}/archive"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_configuration = (
            db.session.query(Configuration)
            .filter_by(id=self.public_configuration.id)
            .one()
        )
        self.assertTrue(reloaded_configuration.archived)
        self.assertEqual(
            reloaded_configuration.update_description, "archive;basic data"
        )
        self.assertEqual(reloaded_configuration.updated_by_id, self.super_user.id)

    def test_post_already_archived(self):
        """Ensure that it doesn't matter if the configuration is already archived."""
        self.public_configuration.archived = True
        db.session.add(self.public_configuration)
        db.session.commit()

        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.public_configuration.id}/archive"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_configuration = (
            db.session.query(Configuration)
            .filter_by(id=self.public_configuration.id)
            .one()
        )
        self.assertTrue(reloaded_configuration.archived)
        self.assertEqual(reloaded_configuration.update_description, "create;basic data")
        self.assertIsNone(reloaded_configuration.updated_by_id)

    def test_post_configuration_super_user_conflict_due_to_device_mount_without_end(
        self,
    ):
        """Ensure that we can't archive a configuration if there is a device mount without end."""
        device_mount_action = DeviceMountAction(
            device=self.public_device,
            configuration=self.public_configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(device_mount_action)
        db.session.commit()
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.public_configuration.id}/archive"
            )
        self.assertEqual(response.status_code, 409)

    def test_post_configuration_super_user_conflict_due_to_device_mount_end_in_the_future(
        self,
    ):
        """Ensure we can't archive a configuration if a device mount ends in the future."""
        device_mount_action = DeviceMountAction(
            device=self.public_device,
            configuration=self.public_configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2012, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
            end_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(device_mount_action)
        db.session.commit()
        with patch.object(
            AllDeviceMountsForConfigurationAreFinishedInThePast,
            "_get_current_date_time",
        ) as mock:
            mock.return_value = datetime.datetime(2022, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
            with self.run_requests_as(self.super_user):
                response = self.client.post(
                    f"{self.configurations_url}/{self.public_configuration.id}/archive"
                )
        self.assertEqual(response.status_code, 409)

    def test_post_configuration_super_user_conflict_due_to_platform_mount_without_end(
        self,
    ):
        """Ensure we can't archive a configuration if a platform mount doesn't end."""
        platform_mount_action = PlatformMountAction(
            platform=self.public_platform,
            configuration=self.public_configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(platform_mount_action)
        db.session.commit()
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.public_configuration.id}/archive"
            )
        self.assertEqual(response.status_code, 409)

    def test_post_configuration_super_user_conflict_due_to_platform_mount_end_in_the_future(
        self,
    ):
        """Ensure we can't archive a configuration if a platform mount ends in the future."""
        platform_mount_action = PlatformMountAction(
            platform=self.public_platform,
            configuration=self.public_configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Mount without end",
            begin_date=datetime.datetime(2012, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
            end_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(platform_mount_action)
        db.session.commit()
        with patch.object(
            AllPlatformMountsForConfigurationAreFinishedInThePast,
            "_get_current_date_time",
        ) as mock:
            mock.return_value = datetime.datetime(2022, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
            with self.run_requests_as(self.super_user):
                response = self.client.post(
                    f"{self.configurations_url}/{self.public_configuration.id}/archive"
                )
        self.assertEqual(response.status_code, 409)

    def test_post_configuration_super_user_conflict_due_to_static_location_without_end(
        self,
    ):
        """Ensure we can't archive a configuration if a static location doesn't end."""
        static_location = ConfigurationStaticLocationBeginAction(
            configuration=self.public_configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Location without end",
            begin_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(static_location)
        db.session.commit()
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.public_configuration.id}/archive"
            )
        self.assertEqual(response.status_code, 409)

    def test_post_configuration_super_user_conflict_due_to_static_location_end_in_the_future(
        self,
    ):
        """Ensure we can't archive configurations if a static location ends in the future."""
        static_location = ConfigurationStaticLocationBeginAction(
            configuration=self.public_configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Location with end",
            begin_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
            end_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(static_location)
        db.session.commit()
        with patch.object(
            AllStaticLocationsForConfigurationAreFinishedInThePast,
            "_get_current_date_time",
        ) as mock:
            mock.return_value = datetime.datetime(2022, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
            with self.run_requests_as(self.super_user):
                response = self.client.post(
                    f"{self.configurations_url}/{self.public_configuration.id}/archive"
                )
        self.assertEqual(response.status_code, 409)

    def test_post_configuration_super_user_conflict_due_to_dynamic_location_without_end(
        self,
    ):
        """Ensure we can't archive a configuration if a dynamic location doesn't end."""
        dynamic_location = ConfigurationDynamicLocationBeginAction(
            configuration=self.public_configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Location with end",
            begin_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(dynamic_location)
        db.session.commit()
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.public_configuration.id}/archive"
            )
        self.assertEqual(response.status_code, 409)

    def test_post_configuration_super_user_conflict_due_to_dynamic_location_end_in_the_future(
        self,
    ):
        """Ensure we can't archive configurations if a dynamic location end is in the future."""
        dynamic_location = ConfigurationDynamicLocationBeginAction(
            configuration=self.public_configuration,
            begin_contact=self.normal_user.contact,
            begin_description="Location with end",
            begin_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
            end_date=datetime.datetime(2022, 9, 8, 12, 0, 0, tzinfo=pytz.UTC),
        )
        db.session.add(dynamic_location)
        db.session.commit()
        with patch.object(
            AllDynamicLocationsForConfigurationAreFinishedInThePast,
            "_get_current_date_time",
        ) as mock:
            mock.return_value = datetime.datetime(2022, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
            with self.run_requests_as(self.super_user):
                response = self.client.post(
                    f"{self.configurations_url}/{self.public_configuration.id}/archive"
                )
        self.assertEqual(response.status_code, 409)
