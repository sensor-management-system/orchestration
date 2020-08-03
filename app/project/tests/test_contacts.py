import json
import unittest

from project.api.models.contact import Contact
from project.api.schemas.contact_schema import ContactSchema
from project.tests.base import BaseTestCase


class TestContactServices(BaseTestCase):
    """
    Test Contact Services
    """
    contact_url = '/contacts'
    object_type = 'contact'

    def test_get_devices(self):
        """Ensure the /contacts route behaves correctly."""
        response = self.client.get('/sis/v1/contacts')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("http://localhost/sis/v1/contacts",
                      data['links']['self'])
        # super().tear_down()

    def test_add_contact_model(self):
        """""Ensure Add platform model """
        contact = Contact(id=45, username='test',
                          email="test@test.test")
        ContactSchema().dump(contact)

    def test_add_contact(self):
        """Ensure a new contact can be added to the database."""

        contact_data = {
            "data": {
                "type": "contact",
                "attributes": {
                    "email": "test"
                }
            }
        }
        super().add_object(
            url=self.contact_url, data_object=contact_data,
            object_type=self.object_type)

    def test_add_contact_invalid_type(self):
        """Ensure error is thrown if the JSON object
         has invalid type."""

        contact_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "email": "test"
                }
            }
        }
        with self.client:
            data, response = super().prepare_response(
                url=self.contact_url, data_object=contact_data)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"contact\".",
                      data['errors'][0]['detail'])

    def test_add_contact_missing_data(self):
        """Ensure error is thrown if the JSON object
        has messing required data."""

        contact_data = {
            "data": {
                "type": "contact",
                "attributes": {
                    "username": "testUser"
                }
            }
        }
        with self.client:
            data, response = super().prepare_response(
                url=self.contact_url, data_object=contact_data)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      data['errors'][0]['detail'])

    def test_add_contact_invalid_json(self):
        """Ensure error is thrown if the JSON object invalid."""

        contact_data = {}
        with self.client:
            data, response = super().prepare_response(
                url=self.contacts_url, data_object=contact_data)
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.",
                      data['errors'][0]['detail'])

    def test_add_contact_invalid_data_key(self):
        """Ensure error is thrown if the JSON object
        has invalid data key."""

        contact_data = {
            "data": {
                "type": "contact",
                "attributes": {
                    "email": 123
                }
            }
        }

        super().add_object_invalid_data_key(
            url=self.attachment_url, data_object=contact_data)


if __name__ == '__main__':
    unittest.main()
