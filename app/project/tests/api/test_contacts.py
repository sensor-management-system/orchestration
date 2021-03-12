import json

from project import base_url
from project.api.models import Contact
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, generate_token_data


def add_a_contact():
    mock_jwt = generate_token_data()
    contact = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
    )
    db.session.add(contact)
    db.session.commit()
    return contact


class TestContactServices(BaseTestCase):
    """
    Test Contact Services
    """

    url = base_url + "/contacts"
    object_type = "contact"
    json_data_url = "/usr/src/app/project/tests/drafts/contacts_test_data.json"

    def test_get_contacts(self):
        """Ensure the /contacts route behaves correctly."""
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [])

    def test_get_collection_of_contacts(self):
        """Ensure contact get collection behaves correctly."""
        contact = add_a_contact()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(contact.email, data["data"][0]["attributes"]["email"])

    def test_post_a_contact(self):
        """Ensure post a contact behaves correctly."""
        mock_jwt = generate_token_data()
        contact = {
            "given_name": mock_jwt["given_name"],
            "family_name": mock_jwt["family_name"],
            "email": mock_jwt["email"],
        }

        data = {"data": {"type": "contact", "attributes": contact}}
        super().add_object(url=self.url, data_object=data, object_type=self.object_type)

    def test_update_a_contact(self):
        """Ensure update contact behaves correctly."""
        contact = add_a_contact()
        contact_updated = {
            "data": {
                "type": "contact",
                "id": contact.id,
                "attributes": {
                    "given_name": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{contact.id}",
            data_object=contact_updated,
            object_type=self.object_type,
        )

    def test_delete_a_contacts(self):
        """Ensure remove contact behaves correctly."""

        contact = add_a_contact()
        _ = super().delete_object(
            url=f"{self.url}/{contact.id}",
        )
