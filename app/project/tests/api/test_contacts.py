import json

from project import base_url
from project.api.models import Contact
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, generate_token_data


def add_a_contact():
    jwt1 = generate_token_data()
    c = Contact(
        given_name=jwt1["given_name"],
        family_name=jwt1["family_name"],
        email=jwt1["email"],
    )
    db.session.add(c)
    db.session.commit()
    return c


class TestContactServices(BaseTestCase):
    """
    Test Contact Services
    """

    contact_url = base_url + "/contacts"
    object_type = "contact"
    json_data_url = "/usr/src/app/project/tests/drafts/contacts_test_data.json"

    def test_get_contacts(self):
        """Ensure the /contacts route behaves correctly."""
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [])

    def test_get_collection_of_contacts(self):
        """Ensure contact get collection behaves correctly."""
        c = add_a_contact()
        response = self.client.get(self.contact_url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(c.email, data["data"][0]["attributes"]["email"])

    def test_post_a_contact(self):
        """Ensure post a contact behaves correctly."""
        jwt1 = generate_token_data()
        c = {
            "given_name": jwt1["given_name"],
            "family_name": jwt1["family_name"],
            "email": jwt1["email"],
        }

        data = {"data": {"type": "contact", "attributes": c}}
        super().add_object(
            url=self.contact_url, data_object=data, object_type=self.object_type
        )

    def test_update_a_contact(self):
        """Ensure update contact behaves correctly."""
        c = add_a_contact()
        c_updated = {
            "data": {
                "type": "contact",
                "id": c.id,
                "attributes": {
                    "given_name": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.contact_url}/{c.id}",
            data_object=c_updated,
            object_type=self.object_type,
        )

    def test_delete_a_contacts(self):
        """Ensure remove contact behaves correctly."""

        c = add_a_contact()
        _ = super().delete_object(
            url=f"{self.contact_url}/{c.id}",
        )
