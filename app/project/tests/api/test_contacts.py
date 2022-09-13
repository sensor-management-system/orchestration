import json
import os

from project import base_url
from project.tests.base import (
    BaseTestCase,
    generate_userinfo_data,
    test_file_path,
    fake,
)
from project.tests.permissions import create_a_test_contact


class TestContactServices(BaseTestCase):
    """
    Test Contact Services
    """

    url = base_url + "/contacts"
    object_type = "contact"
    json_data_url = os.path.join(test_file_path, "drafts", "contacts_test_data.json")

    def test_get_contacts(self):
        """Ensure the /contacts route behaves correctly."""
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [])

    def test_get_collection_of_contacts(self):
        """Ensure contact get collection behaves correctly."""
        contact = create_a_test_contact()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(contact.email, data["data"][0]["attributes"]["email"])

    def test_post_a_contact(self):
        """Ensure post a contact behaves correctly."""
        userinfo = generate_userinfo_data()
        contact = {
            "given_name": userinfo["given_name"],
            "family_name": userinfo["family_name"],
            "email": userinfo["email"],
        }

        data = {"data": {"type": "contact", "attributes": contact}}
        super().add_object(url=self.url, data_object=data, object_type=self.object_type)

    def test_update_a_contact(self):
        """Ensure update contact behaves correctly."""
        contact = create_a_test_contact()
        contact_updated = {
            "data": {
                "type": "contact",
                "id": contact.id,
                "attributes": {"given_name": "updated",},
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{contact.id}",
            data_object=contact_updated,
            object_type=self.object_type,
        )

    def test_delete_a_contacts(self):
        """Ensure remove contact behaves correctly."""

        contact = create_a_test_contact()
        _ = super().delete_object(url=f"{self.url}/{contact.id}",)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
