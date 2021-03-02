"""Tests for the platform attachment endpoints."""

import json
import unittest

from project import base_url
from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.models.platform_attachment import PlatformAttachment
from project.tests.base import BaseTestCase, create_token, query_result_to_list


class TestPlatformAttachmentServices(BaseTestCase):
    """Test platform attachments."""

    def test_add_platform_attachment_api(self):
        """Ensure that we can add a platform attachment."""
        # First we need to make sure that we have a platform
        platform = Platform(
            short_name="Very new platform",
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
        # For converting it to a list
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

    def test_get_platform_attachment_api(self):
        """Ensure that we can get a list of platform attachments."""
        platform1 = Platform(short_name="Just a platform")
        platform2 = Platform(short_name="Another platform")

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

            one_attachment_checked_in_detail = False
            for attachment in payload["data"]:
                attachment["id"] in [str(pa.id) for pa in all_platform_attachments]
                attachment["attributes"]["url"] in [
                    pa.url for pa in all_platform_attachments
                ]
                attachment["attributes"]["label"] in [
                    pa.label for pa in all_platform_attachments
                ]

                if attachment["id"] == str(platform_attachment1.id):
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
                    one_attachment_checked_in_detail = True

            self.assertTrue(one_attachment_checked_in_detail)
