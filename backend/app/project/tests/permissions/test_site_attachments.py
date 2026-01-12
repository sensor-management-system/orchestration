# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the permission handling for site attachment resources."""

import json

from project import base_url
from project.api.models import (
    Contact,
    PermissionGroup,
    PermissionGroupMembership,
    Site,
    SiteAttachment,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list
from project.tests.permissions import create_a_test_site


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
        site = create_a_test_site([str(self.permission_group.id)])
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
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
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
        site = create_a_test_site([str(self.permission_group.id)])
        site.archived = True
        db.session.add(site)
        db.session.commit()
        payload = prepare_site_attachment_payload(site)
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_post_to_a_site_with_an_other_permission_group(self):
        """Post to a site with a different permission Group from the user."""
        site = create_a_test_site([(str(self.other_group.id))])
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
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_a_site_with_a_permission_group(self):
        """Patch attachment of site with same group as user."""
        site = create_a_test_site([str(self.permission_group.id)])
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
        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(attachment.label, data["data"]["attributes"]["label"])
        self.assertEqual(attachment.url, data["data"]["attributes"]["url"])
        self.assertEqual(attachment.site_id, site.id)

    def test_patch_to_archived_site(self):
        """Ensure that we can't patch if the site is archived."""
        site = create_a_test_site([str(self.permission_group.id)])
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
        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_to_a_site_with_a_permission_group(self):
        """Delete attachment of site with same group as user (user is admin)."""
        site = create_a_test_site([str(self.permission_group.id)])
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

        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
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

    def test_delete_for_archived_site(self):
        """Ensure we can't delete for an archived site."""
        site = create_a_test_site([str(self.permission_group.id)])
        attachment = SiteAttachment(
            label=fake.pystr(),
            url=fake.url(),
            site=site,
        )
        site.archived = True
        db.session.add_all([attachment, site])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_non_editable_site(self):
        """Ensure we can't update to a site we can't edit."""
        site1 = create_a_test_site(
            public=False,
            internal=True,
        )
        site1.group_ids = [str(self.permission_group.id)]
        site2 = create_a_test_site(
            public=False,
            internal=True,
        )
        site2.group_ids = [str(self.other_group.id)]
        attachment = SiteAttachment(
            url="https://gfz.potsdam.de",
            label="gfz",
            site=site1,
        )
        db.session.add_all([site1, site2, attachment])
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

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.url}/{attachment.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)
