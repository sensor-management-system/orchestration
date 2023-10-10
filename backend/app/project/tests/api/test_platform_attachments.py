# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the platform attachment endpoints."""

import json
import time
from unittest.mock import patch

from flask import url_for

from project import base_url
from project.api import minio
from project.api.models import Contact, Platform, PlatformAttachment, User
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list


class TestPlatformAttachmentServices(BaseTestCase):
    """Test platform attachments."""

    url = base_url + "/platform-attachments"

    def test_post_platform_attachment_api(self):
        """Ensure that we can add a platform attachment."""
        # First we need to make sure that we have a platform
        platform = Platform(
            short_name="Very new platform",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(platform)
        db.session.commit()

        # Now as it is saved we can be sure that has an id
        self.assertTrue(platform.id is not None)

        count_platform_attachments = (
            db.session.query(PlatformAttachment)
            .filter_by(
                platform_id=platform.id,
            )
            .count()
        )
        # However, this new platform for sure has no attachments
        self.assertEqual(count_platform_attachments, 0)

        # Now we can write the request to add a platform attachment
        payload = {
            "data": {
                "type": "platform_attachment",
                "attributes": {
                    "url": "https://www.gfz-potsdam.de",
                    "label": "GFZ Homepage",
                    "description": "The GFZ homepage",
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": str(platform.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/platform-attachments"
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
        platform_attachments = query_result_to_list(
            db.session.query(PlatformAttachment).filter_by(
                platform_id=platform.id,
            )
        )
        # We now have one attachment
        self.assertEqual(len(platform_attachments), 1)

        # And it is as we specified it
        platform_attachment = platform_attachments[0]
        self.assertEqual(platform_attachment.url, "https://www.gfz-potsdam.de")
        self.assertEqual(platform_attachment.label, "GFZ Homepage")
        self.assertEqual(platform_attachment.description, "The GFZ homepage")
        self.assertEqual(platform_attachment.platform_id, platform.id)
        self.assertEqual(
            str(platform_attachment.platform_id), response.get_json()["data"]["id"]
        )
        msg = "create;attachment"
        self.assertEqual(msg, platform_attachment.platform.update_description)

    def test_post_platform_attachment_api_missing_url(self):
        """Ensure that we don't add a platform attachment with missing url."""
        platform = Platform(
            short_name="Very new platform",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(platform)
        db.session.commit()

        # Now we can write the request to add a platform attachment
        payload = {
            "data": {
                "type": "platform_attachment",
                "attributes": {
                    "url": None,
                    "label": "GFZ Homepage",
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": str(platform.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/platform-attachments"
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
            db.session.query(PlatformAttachment)
            .filter_by(
                platform_id=platform.id,
            )
            .count()
        )
        self.assertEqual(count_attachments, 0)

    def test_post_platform_attachment_api_missing_platform(self):
        """Ensure that we don't add a platform attachment with missing platform."""
        count_platform_attachments_before = db.session.query(PlatformAttachment).count()
        payload = {
            "data": {
                "type": "platform_attachment",
                "attributes": {
                    "url": "GFZ",
                    "label": "GFZ Homepage",
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": None}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/platform-attachments"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # it will not work, as we miss an important part (the platform)
        self.assertEqual(response.status_code, 422)
        count_platform_attachments_after = db.session.query(PlatformAttachment).count()
        self.assertEqual(
            count_platform_attachments_before, count_platform_attachments_after
        )

    def test_get_platform_attachment_api(self):
        """Ensure that we can get a list of platform attachments."""
        platform1 = Platform(
            short_name="Just a platform",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        platform2 = Platform(
            short_name="Another platform",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        db.session.add(platform1)
        db.session.add(platform2)
        db.session.commit()

        platform_attachment1 = PlatformAttachment(
            label="GFZ",
            url="https://www.gfz-potsdam.de",
            description="The GFZ homepage",
            platform=platform1,
        )
        platform_attachment2 = PlatformAttachment(
            label="UFZ",
            url="https://www.ufz.de",
            platform=platform1,
        )
        platform_attachment3 = PlatformAttachment(
            label="PIK",
            url="https://www.pik-potsdam.de",
            platform=platform2,
        )

        db.session.add(platform_attachment1)
        db.session.add(platform_attachment2)
        db.session.add(platform_attachment3)
        db.session.commit()

        all_platform_attachments = [
            platform_attachment1,
            platform_attachment2,
            platform_attachment3,
        ]

        with self.client:
            response = self.client.get(
                base_url + "/platform-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

            platform_attachment1_data = None
            for attachment in payload["data"]:
                attachment["id"] in [str(pa.id) for pa in all_platform_attachments]
                attachment["attributes"]["url"] in [
                    pa.url for pa in all_platform_attachments
                ]
                attachment["attributes"]["label"] in [
                    pa.label for pa in all_platform_attachments
                ]

                if attachment["id"] == str(platform_attachment1.id):
                    platform_attachment1_data = attachment
                    self.assertEqual(
                        attachment["attributes"]["url"], platform_attachment1.url
                    )
                    self.assertEqual(
                        attachment["attributes"]["label"], platform_attachment1.label
                    )
                    self.assertEqual(
                        attachment["attributes"]["description"], "The GFZ homepage"
                    )
                    # and we want to check the link for the platform as well
                    platform_link = attachment["relationships"]["platform"]["links"][
                        "related"
                    ]
                    resp_platform = self.client.get(
                        platform_link,
                        content_type="application/vnd.api+json",
                    )
                    self.assertEqual(resp_platform.status_code, 200)
                    self.assertEqual(
                        resp_platform.get_json()["data"]["id"],
                        str(platform_attachment1.platform_id),
                    )
                    self.assertEqual(
                        resp_platform.get_json()["data"]["attributes"]["short_name"],
                        platform_attachment1.platform.short_name,
                    )

            self.assertTrue(platform_attachment1_data is not None)

            # Now we tested the get request for the list response
            # It is time to check the detail one as well
            response = self.client.get(
                base_url + "/platform-attachments/" + str(platform_attachment1.id),
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            # I already tested the response for this attachment
            self.assertEqual(response.get_json()["data"], platform_attachment1_data)

            # And now we want to make sure that we already filter the platform attachments
            # with a given platform id
            response = self.client.get(
                base_url + "/platforms/" + str(platform1.id) + "/platform-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 2)
            response = self.client.get(
                base_url + "/platforms/" + str(platform2.id) + "/platform-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

    def test_patch_platform_attachment_api(self):
        """Ensure that we can update a platform attachment."""
        platform1 = Platform(
            short_name="Just a platform",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        platform2 = Platform(
            short_name="Another platform",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )

        db.session.add(platform1)
        db.session.add(platform2)
        db.session.commit()

        platform_attachment1 = PlatformAttachment(
            label="GFZ",
            url="https://www.gfz-potsdam.de",
            platform=platform1,
        )
        db.session.add(platform_attachment1)
        db.session.commit()

        payload = {
            "data": {
                "type": "platform_attachment",
                "id": str(platform_attachment1.id),
                "attributes": {
                    "label": "UFZ",
                    "url": "https://www.ufz.de",
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": str(platform2.id)}}
                },
            }
        }
        with self.client:
            url_patch = (
                base_url + "/platform-attachments/" + str(platform_attachment1.id)
            )
            response = self.client.patch(
                url_patch,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 200)

        platform_attachment_reloaded = (
            db.session.query(PlatformAttachment)
            .filter_by(id=platform_attachment1.id)
            .one()
        )
        self.assertEqual(platform_attachment_reloaded.url, "https://www.ufz.de")
        self.assertEqual(platform_attachment_reloaded.label, "UFZ")
        self.assertEqual(platform_attachment_reloaded.platform_id, platform2.id)

        msg = "update;attachment"
        self.assertEqual(msg, platform_attachment_reloaded.platform.update_description)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    def test_post_platform_attachment_with_no_label(self):
        """Ensure that we can not add a platform attachment without a label."""
        # First we need to make sure that we have a platform
        platform = Platform(
            short_name="Very new platform",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=True,
            is_internal=False,
        )
        db.session.add(platform)
        db.session.commit()
        self.assertTrue(platform.id is not None)
        count_platform_attachments = (
            db.session.query(PlatformAttachment)
            .filter_by(
                platform_id=platform.id,
            )
            .count()
        )
        self.assertEqual(count_platform_attachments, 0)
        payload = {
            "data": {
                "type": "platform_attachment",
                "attributes": {
                    "url": "https://www.ufz.de",
                    "label": None,
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": str(platform.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/platform-attachments"
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
        platform = Platform(
            short_name="a new platform",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(platform)
        db.session.commit()
        self.assertTrue(platform.id is not None)

        with patch.object(minio, "download_endpoint") as mock:
            mock.return_value = "http://minio:8080"
            payload = {
                "data": {
                    "type": "platform_attachment",
                    "attributes": {
                        "url": "http://minio:8080/some-bucket/somefile.txt",
                        "label": "Some upload",
                    },
                    "relationships": {
                        "platform": {
                            "data": {"type": "platform", "id": str(platform.id)}
                        }
                    },
                }
            }
            with self.client:
                url_post = base_url + "/platform-attachments"
                response = self.client.post(
                    url_post,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 201)
        data = response.json
        attachment = (
            db.session.query(PlatformAttachment)
            .filter_by(id=data["data"]["id"])
            .first()
        )
        self.assertTrue(attachment.is_upload)
        self.assertTrue(data["data"]["attributes"]["is_upload"])
        self.assertEqual(
            attachment.internal_url, "http://minio:8080/some-bucket/somefile.txt"
        )
        self.assertFalse("internal_url" in data["data"]["attributes"].keys())
        expected_url = url_for(
            "download.get_platform_attachment_content",
            id=attachment.id,
            filename="somefile.txt",
            _external=True,
        )
        self.assertEqual(expected_url, attachment.url)
        self.assertEqual(attachment.url, data["data"]["attributes"]["url"])

    def test_patch_url_for_uploads(self):
        """Ensure that we can't change the url for uploaded files."""
        platform = Platform(
            short_name="a new platform",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        attachment = PlatformAttachment(
            platform=platform,
            label="File upload",
            url="http://localhost/.../file",
            internal_url="http://minio/.../file",
        )
        db.session.add_all([platform, attachment])
        db.session.commit()

        self.assertTrue(attachment.is_upload)

        payload = {
            "data": {
                "type": "platform_attachment",
                "id": str(attachment.id),
                "attributes": {
                    "label": "UFZ",
                    "url": "https://www.ufz.de",
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": str(platform.id)}}
                },
            }
        }
        with self.client:
            url_patch = base_url + "/platform-attachments/" + str(attachment.id)
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
        platform1 = Platform(short_name="dummy platform", is_public=True)

        db.session.add_all([contact1, contact2, user1, user2, platform1])
        db.session.commit()

        with self.run_requests_as(user1):
            response1 = self.client.post(
                self.url,
                data=json.dumps(
                    {
                        "data": {
                            "type": "platform_attachment",
                            "attributes": {
                                "url": "https://gfz-potsdam.de",
                                "label": "GFZ",
                            },
                            "relationships": {
                                "platform": {
                                    "data": {"type": "platform", "id": platform1.id}
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
                            "type": "platform_attachment",
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
