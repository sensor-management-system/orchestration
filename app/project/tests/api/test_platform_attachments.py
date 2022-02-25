"""Tests for the platform attachment endpoints."""

import json

from project import base_url
from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.models.platform_attachment import PlatformAttachment
from project.tests.base import BaseTestCase, create_token, query_result_to_list


class TestPlatformAttachmentServices(BaseTestCase):
    """Test platform attachments."""

    def test_post_platform_attachment_api(self):
        """Ensure that we can add a platform attachment."""
        # First we need to make sure that we have a platform
        platform = Platform(
            short_name="Very new platform",
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
        self.assertEqual(platform_attachment.platform_id, platform.id)
        self.assertEqual(
            str(platform_attachment.platform_id), response.get_json()["data"]["id"]
        )

    def test_post_platform_attachment_api_missing_url(self):
        """Ensure that we don't add a platform attachment with missing url."""
        platform = Platform(
            short_name="Very new platform",
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
        platform1 = Platform(short_name="Just a platform", is_public=True,
                             is_private=False,
                             is_internal=False, )
        platform2 = Platform(short_name="Another platform", is_public=True,
                             is_private=False,
                             is_internal=False, )

        db.session.add(platform1)
        db.session.add(platform2)
        db.session.commit()

        platform_attachment1 = PlatformAttachment(
            label="GFZ",
            url="https://www.gfz-potsdam.de",
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
        platform1 = Platform(short_name="Just a platform", is_public=False,
                             is_private=False,
                             is_internal=True, )
        platform2 = Platform(short_name="Another platform",
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

    def test_delete_platform_attachment_api(self):
        """Ensure that we can delete a platform attachment."""
        platform1 = Platform(short_name="Just a platform",
                             is_public=False,
                             is_private=False,
                             is_internal=True,
                             )
        db.session.add(platform1)
        db.session.commit()
        platform_attachment1 = PlatformAttachment(
            label="GFZ",
            url="https://www.gfz-potsdam.de",
            platform=platform1,
        )
        db.session.add(platform_attachment1)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url + "/platforms/" + str(platform1.id) + "/platform-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

            response = self.client.delete(
                base_url + "/platform-attachments/" + str(platform_attachment1.id),
                headers=create_token(),
            )

            # I would expect a 204 (no content), but 200 is good as well
            self.assertTrue(response.status_code in [200, 204])

            response = self.client.get(
                base_url + "/platforms/" + str(platform1.id) + "/platform-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 0)

        count_platform_attachments = (
            db.session.query(PlatformAttachment)
                .filter_by(
                platform_id=platform1.id,
            )
                .count()
        )
        self.assertEqual(count_platform_attachments, 0)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
