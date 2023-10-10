# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the site attachment endpoints."""

import json
import time
from unittest.mock import patch

from flask import url_for

from project import base_url
from project.api import minio
from project.api.models import Contact, Site, SiteAttachment, User
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list


class TestSiteAttachmentServices(BaseTestCase):
    """Test site attachments."""

    url = base_url + "/site-attachments"

    def test_post_site_attachment_api(self):
        """Ensure that we can add a site attachment."""
        # First we need to make sure that we have a site
        site = Site(
            label="Very new site",
            is_public=False,
            is_internal=True,
        )
        db.session.add(site)
        db.session.commit()

        # Now as it is saved we can be sure that has an id
        self.assertTrue(site.id is not None)

        count_site_attachments = (
            db.session.query(SiteAttachment)
            .filter_by(
                site_id=site.id,
            )
            .count()
        )
        # However, this new site for sure has no attachments
        self.assertEqual(count_site_attachments, 0)

        # Now we can write the request to add a site attachment
        payload = {
            "data": {
                "type": "site_attachment",
                "attributes": {
                    "url": "https://www.gfz-potsdam.de",
                    "label": "GFZ Homepage",
                    "description": "The GFZ homepage",
                },
                "relationships": {
                    "site": {"data": {"type": "site", "id": str(site.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/site-attachments"
            # You may want to look up self.add_object in the BaseTestCase
            # and compare if something doesn't work anymore
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # We expect that it worked and that we have a new entry
        self.assertEqual(response.status_code, 201)
        # And we want to inspect our attachment list
        site_attachments = query_result_to_list(
            db.session.query(SiteAttachment).filter_by(
                site_id=site.id,
            )
        )
        # We now have one attachment
        self.assertEqual(len(site_attachments), 1)

        # And it is as we specified it
        site_attachment = site_attachments[0]
        self.assertEqual(site_attachment.url, "https://www.gfz-potsdam.de")
        self.assertEqual(site_attachment.label, "GFZ Homepage")
        self.assertEqual(site_attachment.description, "The GFZ homepage")
        self.assertEqual(site_attachment.site_id, site.id)
        self.assertEqual(
            str(site_attachment.site_id),
            response.get_json()["data"]["id"],
        )
        msg = "create;attachment"
        self.assertEqual(msg, site_attachment.site.update_description)

    def test_post_site_attachment_api_missing_url(self):
        """Ensure that we don't add a site attachment with missing url."""
        site = Site(
            label="Very new site",
            is_public=False,
            is_internal=True,
        )
        db.session.add(site)
        db.session.commit()

        # Now we can write the request to add a site attachment
        payload = {
            "data": {
                "type": "site_attachment",
                "attributes": {
                    "url": None,
                    "label": "GFZ Homepage",
                },
                "relationships": {
                    "site": {"data": {"type": "site", "id": str(site.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/site-attachments"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # it will not work, as we miss an important part (the url)
        # 422 => unprocessable entity
        self.assertEqual(response.status_code, 422)
        count_attachments = (
            db.session.query(SiteAttachment)
            .filter_by(
                site_id=site.id,
            )
            .count()
        )
        self.assertEqual(count_attachments, 0)

    def test_post_site_attachment_api_missing_site(self):
        """Ensure that we don't add a site attachment with missing site."""
        count_site_attachments_before = db.session.query(SiteAttachment).count()
        payload = {
            "data": {
                "type": "site_attachment",
                "attributes": {
                    "url": "GFZ",
                    "label": "GFZ Homepage",
                },
                "relationships": {"site": {"data": {"type": "site", "id": None}}},
            }
        }
        with self.client:
            url_post = base_url + "/site-attachments"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # it will not work, as we miss an important part (the site)
        self.assertEqual(response.status_code, 422)
        count_site_attachments_after = db.session.query(SiteAttachment).count()
        self.assertEqual(
            count_site_attachments_before,
            count_site_attachments_after,
        )

    def test_get_site_attachment_api(self):
        """Ensure that we can get a list of site attachments."""
        site1 = Site(
            label="Just a site",
            is_public=True,
            is_internal=False,
        )
        site2 = Site(
            label="Another site",
            is_public=True,
            is_internal=False,
        )

        db.session.add(site1)
        db.session.add(site2)
        db.session.commit()

        site_attachment1 = SiteAttachment(
            label="GFZ",
            url="https://www.gfz-potsdam.de",
            description="The GFZ homepage",
            site=site1,
        )
        site_attachment2 = SiteAttachment(
            label="UFZ",
            url="https://www.ufz.de",
            site=site1,
        )
        site_attachment3 = SiteAttachment(
            label="PIK",
            url="https://www.pik-potsdam.de",
            site=site2,
        )

        db.session.add(site_attachment1)
        db.session.add(site_attachment2)
        db.session.add(site_attachment3)
        db.session.commit()

        all_site_attachments = [
            site_attachment1,
            site_attachment2,
            site_attachment3,
        ]

        with self.client:
            response = self.client.get(
                base_url + "/site-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

            site_attachment1_data = None
            for attachment in payload["data"]:
                attachment["id"] in [str(da.id) for da in all_site_attachments]
                attachment["attributes"]["url"] in [
                    da.url for da in all_site_attachments
                ]
                attachment["attributes"]["label"] in [
                    da.label for da in all_site_attachments
                ]

                if attachment["id"] == str(site_attachment1.id):
                    site_attachment1_data = attachment
                    self.assertEqual(
                        attachment["attributes"]["url"], site_attachment1.url
                    )
                    self.assertEqual(
                        attachment["attributes"]["label"],
                        site_attachment1.label,
                    )
                    self.assertEqual(
                        attachment["attributes"]["description"], "The GFZ homepage"
                    )
                    # and we want to check the link for the site as well
                    site_link = attachment["relationships"]["site"]["links"]["related"]
                    resp_site = self.client.get(
                        site_link,
                        content_type="application/vnd.api+json",
                    )
                    self.assertEqual(resp_site.status_code, 200)
                    self.assertEqual(
                        resp_site.get_json()["data"]["id"],
                        str(site_attachment1.site_id),
                    )
                    self.assertEqual(
                        resp_site.get_json()["data"]["attributes"]["label"],
                        site_attachment1.site.label,
                    )

            self.assertTrue(site_attachment1_data is not None)

            # Now we tested the get request for the list response
            # It is time to check the detail one as well
            response = self.client.get(
                base_url + "/site-attachments/" + str(site_attachment1.id),
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            # I already tested the response for this attachment
            self.assertEqual(response.get_json()["data"], site_attachment1_data)

            # And now we want to make sure that we already filter the site attachments
            # with a given site id
            response = self.client.get(
                base_url + "/sites/" + str(site1.id) + "/site-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 2)
            response = self.client.get(
                base_url + "/sites/" + str(site2.id) + "/site-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

    def test_patch_site_attachment_api(self):
        """Ensure that we can update a site attachment."""
        site1 = Site(
            label="Just a site",
            is_public=False,
            is_internal=True,
        )
        site2 = Site(
            label="Another site",
            is_public=False,
            is_internal=True,
        )

        db.session.add(site1)
        db.session.add(site2)
        db.session.commit()

        site_attachment1 = SiteAttachment(
            label="GFZ",
            url="https://www.gfz-potsdam.de",
            site=site1,
        )
        db.session.add(site_attachment1)
        db.session.commit()

        payload = {
            "data": {
                "type": "site_attachment",
                "id": str(site_attachment1.id),
                "attributes": {
                    "label": "UFZ",
                    "url": "https://www.ufz.de",
                },
                "relationships": {
                    "site": {"data": {"type": "site", "id": str(site2.id)}}
                },
            }
        }
        with self.client:
            url_patch = base_url + "/site-attachments/" + str(site_attachment1.id)
            response = self.client.patch(
                url_patch,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 200)

        site_attachment_reloaded = (
            db.session.query(SiteAttachment).filter_by(id=site_attachment1.id).one()
        )
        self.assertEqual(site_attachment_reloaded.url, "https://www.ufz.de")
        self.assertEqual(site_attachment_reloaded.label, "UFZ")
        self.assertEqual(site_attachment_reloaded.site_id, site2.id)
        msg = "update;attachment"
        self.assertEqual(msg, site_attachment_reloaded.site.update_description)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    def test_post_site_attachment_with_no_label(self):
        """Ensure that we can not add a site attachment without a label."""
        site = Site(
            label="anew site",
            is_public=True,
            is_internal=False,
        )
        db.session.add(site)
        db.session.commit()
        self.assertTrue(site.id is not None)

        count_site_attachments = (
            db.session.query(SiteAttachment)
            .filter_by(
                site_id=site.id,
            )
            .count()
        )
        self.assertEqual(count_site_attachments, 0)

        payload = {
            "data": {
                "type": "site_attachment",
                "attributes": {
                    "url": "https://www.ufz.de",
                    "label": None,
                },
                "relationships": {
                    "site": {"data": {"type": "site", "id": str(site.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/site-attachments"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        self.assertEqual(response.status_code, 422)

    def test_post_minio_url(self):
        """
        Test when we post an attachment with a minio url.

        The system should replace the original url with an internal
        one & should set the is_upload entry.
        """
        site = Site(
            label="a new site",
            is_public=True,
            is_internal=False,
        )
        db.session.add(site)
        db.session.commit()
        self.assertTrue(site.id is not None)

        with patch.object(minio, "download_endpoint") as mock:
            mock.return_value = "http://minio:8080"
            payload = {
                "data": {
                    "type": "site_attachment",
                    "attributes": {
                        "url": "http://minio:8080/some-bucket/somefile.txt",
                        "label": "Some upload",
                    },
                    "relationships": {
                        "site": {
                            "data": {
                                "type": "site",
                                "id": str(site.id),
                            }
                        }
                    },
                }
            }
            with self.client:
                url_post = base_url + "/site-attachments"
                response = self.client.post(
                    url_post,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 201)
        data = response.json
        attachment = (
            db.session.query(SiteAttachment).filter_by(id=data["data"]["id"]).first()
        )
        self.assertTrue(attachment.is_upload)
        self.assertTrue(data["data"]["attributes"]["is_upload"])
        self.assertEqual(
            attachment.internal_url, "http://minio:8080/some-bucket/somefile.txt"
        )
        self.assertFalse("internal_url" in data["data"]["attributes"].keys())
        expected_url = url_for(
            "download.get_site_attachment_content",
            id=attachment.id,
            filename="somefile.txt",
            _external=True,
        )
        self.assertEqual(expected_url, attachment.url)
        self.assertEqual(attachment.url, data["data"]["attributes"]["url"])

    def test_patch_url_for_uploads(self):
        """Ensure that we can't change the url for uploaded files."""
        site = Site(
            label="a new site",
            is_public=True,
            is_internal=False,
        )
        attachment = SiteAttachment(
            site=site,
            label="File upload",
            url="http://localhost/.../file",
            internal_url="http://minio/.../file",
        )
        db.session.add_all([site, attachment])
        db.session.commit()

        self.assertTrue(attachment.is_upload)

        payload = {
            "data": {
                "type": "site_attachment",
                "id": str(attachment.id),
                "attributes": {
                    "label": "UFZ",
                    "url": "https://www.ufz.de",
                },
                "relationships": {
                    "site": {"data": {"type": "site", "id": str(site.id)}}
                },
            }
        }
        with self.client:
            url_patch = base_url + "/site-attachments/" + str(attachment.id)
            response = self.client.patch(
                url_patch,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 409)

    def test_created_and_updated_fields(self):
        """Ensure we set & update the created & updated metainformation."""
        contact1 = Contact(
            given_name="first", family_name="contact", email="first@contact.org"
        )
        contact2 = Contact(
            given_name="second", family_name="contact", email="second@contact.org"
        )
        user1 = User(contact=contact1, subject=contact1.email, is_superuser=True)
        user2 = User(contact=contact2, subject=contact2.email, is_superuser=True)
        site1 = Site(label="dummy site", is_public=True)

        db.session.add_all([contact1, contact2, user1, user2, site1])
        db.session.commit()

        with self.run_requests_as(user1):
            response1 = self.client.post(
                self.url,
                data=json.dumps(
                    {
                        "data": {
                            "type": "site_attachment",
                            "attributes": {
                                "url": "https://gfz-potsdam.de",
                                "label": "GFZ",
                            },
                            "relationships": {
                                "site": {
                                    "data": {
                                        "type": "site",
                                        "id": site1.id,
                                    }
                                }
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response1.status_code, 201)
        attachment_id = response1.json["data"]["id"]

        one_second = 1
        time.sleep(one_second)

        with self.run_requests_as(user2):
            response2 = self.client.patch(
                f"{self.url}/{attachment_id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "site_attachment",
                            "id": attachment_id,
                            "attributes": {
                                "label": "GFZ Landing page",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response2.status_code, 200)

        self.assertEqual(
            response1.json["data"]["attributes"]["created_at"],
            response2.json["data"]["attributes"]["created_at"],
        )

        self.assertEqual(
            response1.json["data"]["relationships"]["created_by"]["data"]["id"],
            response2.json["data"]["relationships"]["created_by"]["data"]["id"],
        )
        self.assertEqual(
            response1.json["data"]["relationships"]["created_by"]["data"]["id"],
            str(user1.id),
        )

        self.assertEqual(
            response2.json["data"]["relationships"]["updated_by"]["data"]["id"],
            str(user2.id),
        )

        self.assertTrue(
            # Due to the iso format it is enought to compare them as stirngs
            # here, as 2023-03-14T12:00:00 is < then 2023-03-14T12:00:01.
            response1.json["data"]["attributes"]["updated_at"]
            < response2.json["data"]["attributes"]["updated_at"]
        )
