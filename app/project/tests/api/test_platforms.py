"""Tests for the platforms."""
import os

from project import base_url
from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.models.platform_attachment import PlatformAttachment
from project.tests.base import BaseTestCase, fake, generate_token_data, test_file_path
from project.tests.read_from_json import extract_data_from_json_file


class TestPlatformServices(BaseTestCase):
    """Test Platform Services."""

    platform_url = base_url + "/platforms"
    contact_url = base_url + "/contacts"
    object_type = "platform"
    json_data_url = os.path.join(test_file_path, "drafts", "platforms_test_data.json")

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
        mock_jwt = generate_token_data()
        contact_data = {
            "data": {
                "type": "contact",
                "attributes": {
                    "given_name": mock_jwt["given_name"],
                    "family_name": mock_jwt["family_name"],
                    "email": mock_jwt["email"],
                    "website": fake.url(),
                },
            }
        }
        contact = super().add_object(
            url=self.contact_url, data_object=contact_data, object_type="contact"
        )
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

        platform = Platform(short_name="platform",
                            is_public=False,
                            is_private=False,
                            is_internal=True,
                            )
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
        platform = Platform(short_name="platform",
                            is_public=False,
                            is_private=False,
                            is_internal=True,
                            )
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
