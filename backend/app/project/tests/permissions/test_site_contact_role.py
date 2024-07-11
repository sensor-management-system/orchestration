# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the site contact roles with permission management."""

import json
from unittest.mock import patch

from project import base_url, db
from project.api.models import Contact, Site, SiteContactRole, User
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase


class TestSiteContactRoles(BaseTestCase):
    """Test class for the site contact permission management."""

    url = base_url + "/site-contact-roles"

    def test_patch_to_non_editable_site(self):
        """Ensure we can't update to a site we can't edit."""
        site1 = Site(
            label="site1",
            is_public=False,
            is_internal=True,
            group_ids=["1"],
        )
        site2 = Site(
            label="site2",
            is_public=False,
            is_internal=True,
            group_ids=["2"],
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
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all([site1, site2, contact, user, role])
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

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[*site1.group_ids],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.url}/{role.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)
