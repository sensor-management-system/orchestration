# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for restoring archived sites."""

import json

from project import base_url
from project.api.models import (
    Contact,
    PermissionGroup,
    PermissionGroupMembership,
    Site,
    User,
)
from project.api.models.base_model import db
from project.extensions.instances import mqtt
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
        self.permission_group = PermissionGroup(name="test", entitlement="test")
        self.other_group = PermissionGroup(name="other", entitlement="other")
        self.membership = PermissionGroupMembership(
            permission_group=self.permission_group, user=self.normal_user
        )

        db.session.add_all(
            [
                self.internal_site,
                self.public_site,
                self.normal_contact,
                self.normal_user,
                self.super_contact,
                self.super_user,
                self.permission_group,
                self.other_group,
                self.membership,
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

    def test_post_user_not_in_any_group(self):
        """Ensure that an ordinary user without group membership can't restore."""
        self.public_site.group_ids = [str(self.other_group.id)]
        db.session.add(self.public_site)
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                f"{self.sites_url}/{self.public_site.id}/restore"
            )
        self.assertEqual(response.status_code, 403)

    def test_post_member_in_a_group(self):
        """Ensure that we can unset the archived flag as members."""
        self.public_site.group_ids = [str(self.permission_group.id)]
        db.session.add(self.public_site)
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                f"{self.sites_url}/{self.public_site.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_site = db.session.query(Site).filter_by(id=self.public_site.id).one()
        self.assertFalse(reloaded_site.archived)
        self.assertEqual(reloaded_site.update_description, "restore;basic data")
        self.assertEqual(reloaded_site.updated_by_id, self.normal_user.id)
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called_once()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/patch-site")
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal("site")
        self.expect(notification_data["attributes"]["archived"]).to_equal(False)
        self.expect(notification_data["attributes"]["label"]).to_equal(
            self.public_site.label
        )

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
