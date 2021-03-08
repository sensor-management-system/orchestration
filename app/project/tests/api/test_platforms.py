import unittest

from project import base_url
from project.api.models import Contact
from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.schemas.platform_schema import PlatformSchema
from project.tests.base import BaseTestCase
from project.tests.base import generate_token_data
from project.tests.read_from_json import extract_data_from_json_file


class TestPlatformServices(BaseTestCase):
    """
    Test Event Services
    """

    platform_url = base_url + "/platforms"
    object_type = "platform"
    json_data_url = "/usr/src/app/project/tests/drafts/platforms_test_data.json"

    def test_add_platform_model(self):
        """""Ensure Add platform model """
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


if __name__ == "__main__":
    unittest.main()
