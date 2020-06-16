import unittest

from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.schemas.contact_schema import ContactSchema
from project.tests.base import BaseTestCase
from project.tests.read_from_json import extract_data_from_json_file
from project.urls import base_url


class TestContactServices(BaseTestCase):
    """
    Test Contact Services
    """
    contact_url = base_url + '/contacts'
    object_type = 'contact'
    json_data_url = "/usr/src/app/project/tests/drafts/contacts_test_data.json"

    def test_get_contacts(self):
        """Ensure the /contacts route behaves correctly."""
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)

    def test_add_contact_model(self):
        """""Ensure Add platform model """
        contact = Contact(id=45, given_name='test_user',
                          family_name='Test',
                          website='http://test.de',
                          email="test@test.test")
        ContactSchema().dump(contact)
        db.session.add(contact)
        db.session.commit()

        c = db.session.query(Contact).filter_by(
            id=contact.id).one()
        self.assertIn(c.email, contact.email)
        return contact

    def test_add_contact(self):
        """Ensure a new contact can be added to the database."""
        contact_json = extract_data_from_json_file(
            self.json_data_url,
            "contacts")

        contact_data = {
            "data": {
                "type": "contact",
                "attributes": contact_json[0]
            }
        }
        super().add_object(
            url=self.contact_url, data_object=contact_data,
            object_type=self.object_type)
        return contact_data


if __name__ == '__main__':
    unittest.main()
