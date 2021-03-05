"""Tests for the platforms."""

import unittest

from project import base_url
from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.models.platform_attachment import PlatformAttachment
from project.api.schemas.platform_schema import PlatformSchema
from project.tests.base import BaseTestCase
from project.tests.read_from_json import extract_data_from_json_file
from project.tests.test_contacts import TestContactServices


class TestPlatformServices(BaseTestCase):
    """Test Platform Services."""

    platform_url = base_url + "/platforms"
    object_type = "platform"
    json_data_url = "/usr/src/app/project/tests/drafts/platforms_test_data.json"

    def test_add_platform_model(self):
        """Ensure Add platform model."""
        platform = Platform(
            id=13,
            short_name="short_name test",
            description="description test",
            long_name="long_name test",
            manufacturer_name="manufacturer_name test",
            manufacturer_uri="http://cv.de/manufacturer_uri",
            model="model test",
            platform_type_uri="http://cv.de/platform_type_uri",
            platform_type_name="platform_type_name test",
            status_uri="http://cv.de/status_uri test",
            status_name="status_name test",
            website="http://website.de/platform",
            inventory_number="inventory_number test",
            serial_number="serial_number test",
            persistent_identifier="persistent_identifier_test",
        )
        PlatformSchema().dump(platform)
        db.session.add(platform)
        db.session.commit()

        p = db.session.query(Platform).filter_by(id=platform.id).one()
        self.assertIn(p.persistent_identifier, "persistent_identifier_test")

    def test_add_platform(self):
        """Ensure a new platform can be added to the database."""
        platforms_json = extract_data_from_json_file(self.json_data_url, "platforms")

        platform_data = {"data": {"type": "platform", "attributes": platforms_json[0]}}

        super().add_object(
            url=self.platform_url,
            data_object=platform_data,
            object_type=self.object_type,
        )

    def test_add_platform_contacts_relationship(self):
        """Ensure a new relationship between a platform & contact can be created."""
        contact_service = TestContactServices()
        # We need to inject the client (not done on just creating the contact_service)
        contact_service.client = self.client
        contact = contact_service.test_add_contact()
        platform_json = extract_data_from_json_file(self.json_data_url, "platforms")

        platform_data = {
            "data": {
                "type": "platform",
                "attributes": platform_json[0],
                "relationships": {
                    "contacts": {
                        "data": [{"type": "contact", "id": contact["data"]["id"]}]
                    },
                },
            }
        }
        data = super().add_object(
            url=self.platform_url + "?include=contacts",
            data_object=platform_data,
            object_type=self.object_type,
        )

        result_contact_ids = [
            x["id"] for x in data["data"]["relationships"]["contacts"]["data"]
        ]

        self.assertIn(contact["data"]["id"], result_contact_ids)

    def test_add_platform_platform_attachment_included(self):
        """Ensure that we can include attachments on getting a platform."""
        # We want to create here a platform, add two platform attachments
        # and want to make sure that we can query the attachments
        # together with the platform itself.

        platform = Platform(short_name="platform")
        db.session.add(platform)

        attachment1 = PlatformAttachment(
            url="www.gfz-potsdam.de", label="GFZ", platform=platform
        )
        db.session.add(attachment1)
        attachment2 = PlatformAttachment(
            url="www.ufz.de", label="UFZ", platform=platform
        )
        db.session.add(attachment2)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url
                + "/platforms/"
                + str(platform.id)
                + "?include=platform_attachments",
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()

        self.assertEqual(response_data["data"]["id"], str(platform.id))

        attachment_ids = [
            x["id"]
            for x in response_data["data"]["relationships"]["platform_attachments"][
                "data"
            ]
        ]

        self.assertEqual(len(attachment_ids), 2)

        for attachment in [attachment1, attachment2]:
            self.assertIn(str(attachment.id), attachment_ids)

        included_attachments = {}

        for included_entry in response_data["included"]:
            if included_entry["type"] == "platform_attachment":
                attachment_id = included_entry["id"]
                included_attachments[attachment_id] = included_entry

        self.assertEqual(len(included_attachments.keys()), 2)

        for attachment in [attachment1, attachment2]:
            self.assertIn(str(attachment.id), included_attachments.keys())
            self.assertEqual(
                attachment.url,
                included_attachments[str(attachment.id)]["attributes"]["url"],
            )
            self.assertEqual(
                attachment.label,
                included_attachments[str(attachment.id)]["attributes"]["label"],
            )

    def test_add_platform_platform_attachment_relationship(self):
        """Ensure that we can work with the attachment relationship."""
        platform = Platform(short_name="platform")
        db.session.add(platform)

        attachment1 = PlatformAttachment(
            url="www.gfz-potsdam.de", label="GFZ", platform=platform
        )
        db.session.add(attachment1)
        attachment2 = PlatformAttachment(
            url="www.ufz.de", label="UFZ", platform=platform
        )
        db.session.add(attachment2)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url
                + "/platforms/"
                + str(platform.id)
                + "/relationships/platform-attachments",
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()

        # it seems that this relationships are plain integer values
        # so we convert them explicitly
        attachment_ids = [str(x["id"]) for x in response_data["data"]]

        self.assertEqual(len(attachment_ids), 2)

        for attachment in [attachment1, attachment2]:
            self.assertIn(str(attachment.id), attachment_ids)


if __name__ == "__main__":
    unittest.main()
