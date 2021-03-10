from project import base_url
from project.api.models import Contact
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, generate_token_data
from project.tests.read_from_json import extract_data_from_json_file


class TestPlatformServices(BaseTestCase):
    """
    Test Event Services
    """

    platform_url = base_url + "/platforms"
    object_type = "platform"
    json_data_url = "/usr/src/app/project/tests/drafts/platforms_test_data.json"

    def test_add_platform(self):
        """Ensure a new platform can be added to the database."""

        platforms_json = extract_data_from_json_file(self.json_data_url, "platforms")

        platform_data = {"data": {"type": "platform", "attributes": platforms_json[0]}}

        super().add_object(
            url=self.platform_url,
            data_object=platform_data,
            object_type=self.object_type,
        )

    def add_platform_contacts_relationship(self):
        """Ensure a new relationship between a platform and a contact
        can be established.
        """
        jwt = generate_token_data()
        contact = Contact(
            given_name=jwt["given_name"],
            family_name=jwt["family_name"],
            email=jwt["email"],
        )
        db.session.add(contact)
        db.session.commit()
        platform_json = extract_data_from_json_file(self.json_data_url, "devices")

        platform_data = {
            "data": {"type": "device", "attributes": platform_json[0]},
            "relationships": {"data": [{"type": "contact", "id": contact.id}]},
        }
        data = super().add_object(
            url=self.platform_url + "?include=contacts",
            data_object=platform_data,
            object_type=self.object_type,
        )

        self.assertIn(
            contact.id, data["data"]["relationships"]["contacts"]["data"]["id"]
        )
