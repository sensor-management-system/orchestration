# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the site contact roles with permission management."""

import json

from project import base_url, db
from project.api.models import (
    Contact,
    PermissionGroup,
    PermissionGroupMembership,
    Site,
    SiteContactRole,
    User,
)
from project.tests.base import BaseTestCase


class TestSiteContactRoles(BaseTestCase):
    """Test class for the site contact permission management."""

    url = base_url + "/site-contact-roles"

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

    def test_patch_to_non_editable_site(self):
        """Ensure we can't update to a site we can't edit."""
        site1 = Site(
            label="site1",
            is_public=False,
            is_internal=True,
            group_ids=[str(self.permission_group.id)],
        )
        site2 = Site(
            label="site2",
            is_public=False,
            is_internal=True,
            group_ids=[str(self.other_group.id)],
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        role = SiteContactRole(
            contact=contact,
            site=site1,
            role_name="Owner",
            role_uri="something",
        )
        db.session.add_all([site1, site2, contact, role])
        db.session.commit()

        payload = {
            "data": {
                "type": "site_contact_role",
                "id": role.id,
                "attributes": {},
                "relationships": {
                    # We try to switch here to another site for
                    # which we have no edit permissions.
                    "site": {
                        "data": {
                            "type": "site",
                            "id": site2.id,
                        }
                    },
                },
            }
        }

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.url}/{role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)
