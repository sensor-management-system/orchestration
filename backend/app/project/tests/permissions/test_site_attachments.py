# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the permission handling for site attachment resources."""

import json
from unittest.mock import patch

from project import base_url
from project.api.models import Contact, Site, SiteAttachment, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list
from project.tests.permissions import create_a_test_site
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def prepare_site_attachment_payload(site):
    """Create some test payload for site attachments."""
    payload = {
        "data": {
            "type": "site_attachment",
            "attributes": {"label": fake.pystr(), "url": fake.url()},
            "relationships": {"site": {"data": {"type": "site", "id": str(site.id)}}},
        }
    }
    return payload


class TestSiteAttachment(BaseTestCase):
    """Test SiteAttachment."""

    url = base_url + "/site-attachments"

    def test_get_public_site_attachments(self):
        """Ensure that we can get a list of public site_attachments."""
        site1 = create_a_test_site(
            public=True,
            internal=False,
        )
        site2 = create_a_test_site(
            public=True,
            internal=False,
        )

        attachment1 = SiteAttachment(
            label=fake.pystr(),
            url=fake.url(),
            site=site1,
        )
        attachment2 = SiteAttachment(
            label=fake.pystr(),
            url=fake.url(),
            site=site1,
        )
        attachment3 = SiteAttachment(
            label=fake.pystr(),
            url=fake.url(),
            site=site2,
        )

        db.session.add_all([attachment1, attachment2, attachment3])
        db.session.commit()

        with self.client:
            response = self.client.get(
                self.url,
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

    def test_get_internal_site_attachments(self):
        """Ensure that we get internal site attachments only for authenticate users."""
        site1 = create_a_test_site(
            public=False,
            internal=True,
        )
        site2 = create_a_test_site(
            public=False,
            internal=True,
        )

        attachment1 = SiteAttachment(
            label=fake.pystr(),
            url=fake.url(),
            site=site1,
        )
        attachment2 = SiteAttachment(
            label=fake.pystr(),
            url=fake.url(),
            site=site2,
        )

        db.session.add_all([attachment1, attachment2])
        db.session.commit()

        with self.client:
            response = self.client.get(
                self.url,
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

    def test_post_to_a_site_with_a_permission_group(self):
        """Post to site,with permission Group."""
        site = create_a_test_site(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(site.id is not None)
        count_site_attachments = (
            db.session.query(SiteAttachment)
            .filter_by(
                site_id=site.id,
            )
            .count()
        )

        self.assertEqual(count_site_attachments, 0)
        payload = prepare_site_attachment_payload(site)
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:

                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 201)
        site_attachments = query_result_to_list(
            db.session.query(SiteAttachment).filter_by(
                site_id=site.id,
            )
        )
        self.assertEqual(len(site_attachments), 1)

        attachment = site_attachments[0]
        self.assertEqual(attachment.label, payload["data"]["attributes"]["label"])
        self.assertEqual(attachment.url, payload["data"]["attributes"]["url"])
        self.assertEqual(attachment.site_id, site.id)
        self.assertEqual(str(attachment.site_id), response.get_json()["data"]["id"])

    def test_post_to_archived_site(self):
        """Ensure that we can't post for an archived site."""
        site = create_a_test_site(IDL_USER_ACCOUNT.membered_permission_groups)
        site.archived = True
        db.session.add(site)
        db.session.commit()
        payload = prepare_site_attachment_payload(site)
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:

                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_post_to_a_site_with_an_other_permission_group(self):
        """Post to a site with a different permission Group from the user."""
        site = create_a_test_site([403])
        self.assertTrue(site.id is not None)
        count_site_attachments = (
            db.session.query(SiteAttachment)
            .filter_by(
                site_id=site.id,
            )
            .count()
        )

        self.assertEqual(count_site_attachments, 0)
        payload = prepare_site_attachment_payload(site)
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_a_site_with_a_permission_group(self):
        """Patch attachment of site with same group as user."""
        site = create_a_test_site(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(site.id is not None)
        count_site_attachments = (
            db.session.query(SiteAttachment)
            .filter_by(
                site_id=site.id,
            )
            .count()
        )

        self.assertEqual(count_site_attachments, 0)
        attachment = SiteAttachment(
            label=fake.pystr(),
            url=fake.url(),
            site=site,
        )
        db.session.add(attachment)
        db.session.commit()
        payload = {
            "data": {
                "id": attachment.id,
                "type": "site_attachment",
                "attributes": {"label": "changed", "url": attachment.url},
                "relationships": {
                    "site": {"data": {"type": "site", "id": str(site.id)}}
                },
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.patch(
                    url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(attachment.label, data["data"]["attributes"]["label"])
        self.assertEqual(attachment.url, data["data"]["attributes"]["url"])
        self.assertEqual(attachment.site_id, site.id)

    def test_patch_to_archived_site(self):
        """Ensure that we can't patch if the site is archived."""
        site = create_a_test_site(IDL_USER_ACCOUNT.membered_permission_groups)
        attachment = SiteAttachment(
            label=fake.pystr(),
            url=fake.url(),
            site=site,
        )
        site.archived = True
        db.session.add_all([attachment, site])
        db.session.commit()
        payload = {
            "data": {
                "id": attachment.id,
                "type": "site_attachment",
                "attributes": {"label": "changed", "url": attachment.url},
                "relationships": {
                    "site": {"data": {"type": "site", "id": str(site.id)}}
                },
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.patch(
                    url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_to_a_site_with_a_permission_group(self):
        """Delete attachment of site with same group as user (user is admin)."""
        site = create_a_test_site(IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertTrue(site.id is not None)
        count_site_attachments = (
            db.session.query(SiteAttachment)
            .filter_by(
                site_id=site.id,
            )
            .count()
        )

        self.assertEqual(count_site_attachments, 0)
        attachment = SiteAttachment(
            label=fake.pystr(),
            url=fake.url(),
            site=site,
        )
        db.session.add(attachment)
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

    def test_delete_for_archived_site(self):
        """Ensure we can't delete for an archived site."""
        site = create_a_test_site(IDL_USER_ACCOUNT.administrated_permission_groups)
        attachment = SiteAttachment(
            label=fake.pystr(),
            url=fake.url(),
            site=site,
        )
        site.archived = True
        db.session.add_all([attachment, site])
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_to_a_site_with_a_permission_group_as_a_member(self):
        """Delete attachment of site with same group as user (user is member)."""
        site = create_a_test_site(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(site.id is not None)
        count_site_attachments = (
            db.session.query(SiteAttachment)
            .filter_by(
                site_id=site.id,
            )
            .count()
        )

        self.assertEqual(count_site_attachments, 0)
        attachment = SiteAttachment(
            label=fake.pystr(),
            url=fake.url(),
            site=site,
        )
        db.session.add(attachment)
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)
        site_reloaded = (
            db.session.query(Site)
            .filter_by(
                id=site.id,
            )
            .first()
        )
        self.assertEqual(site_reloaded.update_description, "delete;attachment")

    def test_patch_to_non_editable_site(self):
        """Ensure we can't update to a site we can't edit."""
        site1 = create_a_test_site(
            public=False,
            internal=True,
        )
        site1.group_ids = ["1"]
        site2 = create_a_test_site(
            public=False,
            internal=True,
        )
        site2.group_ids = ["2"]
        attachment = SiteAttachment(
            url="https://gfz.potsdam.de",
            label="gfz",
            site=site1,
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all([site1, site2, contact, user, attachment])
        db.session.commit()

        payload = {
            "data": {
                "type": "site_attachment",
                "id": attachment.id,
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
                    membered_permission_groups=site1.group_ids,
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.url}/{attachment.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)
