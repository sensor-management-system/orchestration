# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for restoring archived sites."""

from unittest.mock import patch

from project import base_url
from project.api.models import Contact, Site, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase


class TestRestoreSites(BaseTestCase):
    """Test class to restore sites."""

    sites_url = base_url + "/sites"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@somewhere"
        )
        self.super_contact = Contact(
            given_name="super", family_name="contact", email="super.contact@somewhere"
        )
        self.normal_user = User(
            contact=self.normal_contact,
            subject=self.normal_contact.email,
        )
        self.super_user = User(
            contact=self.super_contact,
            subject=self.super_contact.email,
            is_superuser=True,
        )
        self.internal_site = Site(
            label="internal",
            is_internal=True,
            is_public=False,
            created_by=self.normal_user,
            updated_by=self.normal_user,
            archived=True,
            update_description="archived;basic data",
        )
        self.public_site = Site(
            label="public",
            is_internal=False,
            is_public=True,
            created_by=self.normal_user,
            updated_by=self.normal_user,
            archived=True,
            update_description="archved;basic data",
        )

        db.session.add_all(
            [
                self.internal_site,
                self.public_site,
                self.normal_contact,
                self.normal_user,
                self.super_contact,
                self.super_user,
            ]
        )
        db.session.commit()

    def test_get(self):
        """Ensure that it is not allowed to use the get method."""
        response = self.client.get(f"{self.sites_url}/12345/restore")
        self.assertEqual(response.status_code, 405)

    def test_post_unauthorized(self):
        """Ensure that we don't allow anonymous to restore."""
        response = self.client.post(f"{self.sites_url}/12345/restore")
        self.assertEqual(response.status_code, 401)

    def test_post_nonexisting(self):
        """Ensure that we got an 404 when the site doesn't exist."""
        with self.run_requests_as(self.normal_user):
            response = self.client.post(f"{self.sites_url}/12345/restore")
        self.assertEqual(response.status_code, 404)

    def test_post_user_not_in_idl(self):
        """Ensure that an ordinary user without an entry in the idl can't restore."""
        self.public_site.group_ids = ["123"]
        db.session.add(self.public_site)
        db.session.commit()

        with patch.object(
            idl, "get_all_permission_groups_for_a_user", return_value=None
        ):
            with self.run_requests_as(self.normal_user):
                response = self.client.post(
                    f"{self.sites_url}/{self.public_site.id}/restore"
                )
        self.assertEqual(response.status_code, 403)

    def test_post_user_not_in_any_group(self):
        """Ensure that an ordinary user without group membership can't restore."""
        self.public_site.group_ids = ["123"]
        db.session.add(self.public_site)
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
                    f"{self.sites_url}/{self.public_site.id}/restore"
                )
        self.assertEqual(response.status_code, 403)

    def test_post_user_in_a_group(self):
        """Ensure that an ordinary user can't restore."""
        self.public_site.group_ids = ["123"]
        db.session.add(self.public_site)
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
                    f"{self.sites_url}/{self.public_site.id}/restore"
                )
        self.assertEqual(response.status_code, 403)

    def test_post_admin_in_a_group(self):
        """Ensure that we can unset the archived flag as admins."""
        self.public_site.group_ids = ["123"]
        db.session.add(self.public_site)
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
                    f"{self.sites_url}/{self.public_site.id}/restore"
                )
        self.assertEqual(response.status_code, 204)
        reloaded_site = db.session.query(Site).filter_by(id=self.public_site.id).one()
        self.assertFalse(reloaded_site.archived)
        self.assertEqual(reloaded_site.update_description, "restore;basic data")
        self.assertEqual(reloaded_site.updated_by_id, self.normal_user.id)

    def test_post_superuser(self):
        """Ensure that we can unset the archived flag super user."""
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.sites_url}/{self.public_site.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_site = db.session.query(Site).filter_by(id=self.public_site.id).one()
        self.assertFalse(reloaded_site.archived)
        self.assertEqual(reloaded_site.update_description, "restore;basic data")
        self.assertEqual(reloaded_site.updated_by_id, self.super_user.id)

    def test_post_already_restored(self):
        """Ensure that it doesn't matter if the site is not archived at the beginning."""
        self.public_site.archived = False
        self.public_site.update_description = "create;basic data"
        db.session.add(self.public_site)
        db.session.commit()

        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.sites_url}/{self.public_site.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_site = db.session.query(Site).filter_by(id=self.public_site.id).one()
        self.assertFalse(reloaded_site.archived)
        # But we don't change the entity
        self.assertEqual(reloaded_site.update_description, "create;basic data")
        self.assertEqual(reloaded_site.updated_by_id, self.normal_user.id)