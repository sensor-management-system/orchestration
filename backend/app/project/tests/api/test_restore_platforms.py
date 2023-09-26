# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the restoring platforms."""

from unittest.mock import patch

from project import base_url
from project.api.models import Contact, Platform, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase


class TestRestorePlatform(BaseTestCase):
    """Test class to restore platforms."""

    platforms_url = base_url + "/platforms"

    def setUp(self):
        """Set up some data to test with."""
        super().setUp()

        self.public_platform = Platform(
            short_name="simple platform",
            archived=True,
            is_public=True,
            is_private=False,
            is_internal=False,
            update_description="create;basic data",
        )
        self.private_platform = Platform(
            short_name="not so simple platform",
            archived=True,
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
        db.session.add_all(
            [
                self.public_platform,
                self.private_platform,
                contact1,
                contact2,
                self.normal_user,
                self.super_user,
            ]
        )
        db.session.commit()

    def test_get(self):
        """Ensure that it is not allowed to use the get method."""
        response = self.client.get(f"{self.platforms_url}/12345/restore")
        self.assertEqual(response.status_code, 405)

    def test_post_unauthorized(self):
        """Ensure that we don't allow anonymous to restore."""
        response = self.client.post(f"{self.platforms_url}/12345/restore")
        self.assertEqual(response.status_code, 401)

    def test_post_nonexisting(self):
        """Ensure that we got an 404 when the platform doesn't exist."""
        with self.run_requests_as(self.normal_user):
            response = self.client.post(f"{self.platforms_url}/12345/restore")
        self.assertEqual(response.status_code, 404)

    def test_post_user_not_in_idl(self):
        """Ensure that an ordinary user without an entry in the idl can't restore."""
        self.public_platform.group_ids = ["123"]
        db.session.add(self.public_platform)
        db.session.commit()

        with patch.object(
            idl, "get_all_permission_groups_for_a_user", return_value=None
        ):
            with self.run_requests_as(self.normal_user):
                response = self.client.post(
                    f"{self.platforms_url}/{self.public_platform.id}/restore"
                )
            self.assertEqual(response.status_code, 403)

    def test_post_user_not_in_any_group(self):
        """Ensure that an ordinary user without group membership can't restore."""
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
                    f"{self.platforms_url}/{self.public_platform.id}/restore"
                )
            self.assertEqual(response.status_code, 403)

    def test_post_user_in_a_group(self):
        """Ensure that an ordinary user can't restore."""
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
                    f"{self.platforms_url}/{self.public_platform.id}/restore"
                )
            self.assertEqual(response.status_code, 403)

    def test_post_admin_in_a_group(self):
        """Ensure that we can unset the archived flag as admins."""
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
                    f"{self.platforms_url}/{self.public_platform.id}/restore"
                )
        self.assertEqual(response.status_code, 204)
        reloaded_platform = (
            db.session.query(Platform).filter_by(id=self.public_platform.id).one()
        )
        self.assertFalse(reloaded_platform.archived)
        self.assertEqual(reloaded_platform.update_description, "restore;basic data")
        self.assertEqual(reloaded_platform.updated_by_id, self.normal_user.id)

    def test_post_superuser(self):
        """Ensure that we can unset the archived flag super user."""
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.public_platform.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_platform = (
            db.session.query(Platform).filter_by(id=self.public_platform.id).one()
        )
        self.assertFalse(reloaded_platform.archived)
        self.assertEqual(reloaded_platform.update_description, "restore;basic data")
        self.assertEqual(reloaded_platform.updated_by_id, self.super_user.id)

    def test_post_already_restored(self):
        """Ensure that it doesn't matter if the platform is not archived at the beginning."""
        self.public_platform.archived = False
        db.session.add(self.public_platform)
        db.session.commit()

        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.public_platform.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_platform = (
            db.session.query(Platform).filter_by(id=self.public_platform.id).one()
        )
        self.assertFalse(reloaded_platform.archived)
        self.assertEqual(reloaded_platform.update_description, "create;basic data")
        self.assertIsNone(reloaded_platform.updated_by_id)

    def test_post_private_platform_different_user(self):
        """Ensure that a user can't restore a private platform of another user."""
        self.private_platform.created_by_id = self.super_user.id
        db.session.add(self.private_platform)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.private_platform.id}/restore"
            )
        self.assertEqual(response.status_code, 403)

    def test_post_private_platform_same_user(self):
        """Ensure that a user can restore a private platform of her/himself."""
        self.private_platform.created_by_id = self.normal_user.id
        db.session.add(self.private_platform)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.private_platform.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_platform = (
            db.session.query(Platform).filter_by(id=self.private_platform.id).one()
        )
        self.assertFalse(reloaded_platform.archived)
        self.assertEqual(reloaded_platform.update_description, "restore;basic data")
        self.assertEqual(reloaded_platform.updated_by_id, self.normal_user.id)

    def test_post_private_platform_super_user(self):
        """Ensure that a super user can restore a private platform of other users."""
        self.private_platform.created_by_id = self.normal_user.id
        db.session.add(self.private_platform)
        db.session.commit()
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.platforms_url}/{self.private_platform.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_platform = (
            db.session.query(Platform).filter_by(id=self.private_platform.id).one()
        )
        self.assertFalse(reloaded_platform.archived)

        self.assertEqual(reloaded_platform.update_description, "restore;basic data")
        self.assertEqual(reloaded_platform.updated_by_id, self.super_user.id)
