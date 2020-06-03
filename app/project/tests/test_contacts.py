import json
import unittest

from project.api.models.contact import Contact
from project.api.schemas.contact_schema import ContactSchema
from project.tests.base import BaseTestCase


class TestContactServices(BaseTestCase):
    """
    Test Contact Services
    """
    url = '/sis/v1/contacts'
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

        data_object = {
            "data": {
                "type": "contact",
                "attributes": {
                    "email": "test"
                }
            }
        }
        super(TestContactServices, self). \
            test_add_object(url=self.url,
                            data_object=data_object,
                            object_type=self.object_type)

    def test_add_contact_invalid_type(self):
        """Ensure error is thrown if the JSON object
         has invalid type."""

        data_object = {
            "data": {
                "type": "platform",
                "attributes": {
                    "email": "test"
                }
            }
        }
        with self.client:
            data, response = super(TestContactServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"contact\".",
                      data['errors'][0]['detail'])

    def test_add_contact_missing_data(self):
        """Ensure error is thrown if the JSON object
        has messing required data."""

        data_object = {
            "data": {
                "type": "contact",
                "attributes": {
                    "username": "testUser"
                }
            }
        }
        with self.client:
            data, response = super(TestContactServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      data['errors'][0]['detail'])

    def test_add_contact_invalid_json(self):
        """Ensure error is thrown if the JSON object invalid."""

        data_object = {}
        with self.client:
            data, response = super(TestContactServices, self). \
                prepare_response(url=self.contacts_url,
                                 data_object=data_object)
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.",
                      data['errors'][0]['detail'])

    def test_add_contact_invalid_data_key(self):
        """Ensure error is thrown if the JSON object
        has invalid data key."""

        data_object = {
            "data": {
                "type": "contact",
                "attributes": {
                    "email": 123
                }
            }
        }
        with self.client:
            data, response = super(TestContactServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Not a valid string.",
                      data['errors'][0]['detail'])


if __name__ == '__main__':
    unittest.main()
