# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the sites."""
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
from project.tests.base import BaseTestCase


class TestSites(BaseTestCase):
    """Test class for the site permission management."""

    url = base_url + "/sites"

    def setUp(self):
        """Set stuff up for the tests."""
        super().setUp()
        normal_contact = Contact(
            given_name="normal", family_name="user", email="normal.user@localhost"
        )
        self.normal_user = User(subject=normal_contact.email, contact=normal_contact)
        contact = Contact(
            given_name="super", family_name="user", email="super.user@localhost"
        )
        self.super_user = User(
            subject=contact.email, contact=contact, is_superuser=True
        )

        self.permission_group = PermissionGroup(name="test", entitlement="test")
        self.other_group = PermissionGroup(name="other", entitlement="other")
        self.membership = PermissionGroupMembership(
            permission_group=self.permission_group, user=self.normal_user
        )
        db.session.add_all(
            [
                contact,
                normal_contact,
                self.normal_user,
                self.super_user,
                self.permission_group,
                self.other_group,
                self.membership,
            ]
        )
        db.session.commit()

    def test_patch_to_different_permission_group(self):
        """Ensure we can't update to a permission group we aren't members."""
        site = Site(
            label="test site",
            is_public=False,
            is_internal=True,
            group_ids=[str(self.permission_group.id)],
        )
        db.session.add_all([site])
        db.session.commit()

        payload = {
            "data": {
                "type": "site",
                "id": site.id,
                "attributes": {
                    "group_ids": [str(self.other_group.id)],
                },
                "relationships": {},
            }
        }

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.url}/{site.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_with_pid_as_admin(self):
        """Ensure we can't delete a site with a pid even if we are superuspers."""
        site = Site(
            label="test site",
            is_public=False,
            is_internal=True,
            group_ids=["1"],
            persistent_identifier="12345/SMS-111",
        )
        db.session.add_all([site])
        db.session.commit()

        with self.run_requests_as(self.super_user):
            with self.client:
                response = self.client.delete(
                    f"{self.url}/{site.id}",
                )
        self.assertEqual(response.status_code, 403)
