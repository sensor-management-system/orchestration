import json
import unittest

from project.api.models.customfield import CustomField
from project.api.schemas.customfieldSchema import CustomFieldSchema
from project.tests.base import BaseTestCase


class TestFieldServices(BaseTestCase):

    def test_add_attachment_model(self):
        """""Ensure Add an Field model """
        customfield = CustomField(id=5, key='test',
                                  value="test")
        CustomFieldSchema().dump(customfield)

    def test_add_field(self):
        """Ensure a new Field can be added to the database."""

        with self.client:
            response = self.client.post(
                '/sis/v1/customfields',
                data=json.dumps({
                    "data": {
                        "type": "customfield",
                        "attributes": {
                            "key": "testKey1",
                            "value": "testVal1"
                        }
                    }
                }),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('testKey1', data['data']['attributes']['key'])
        self.assertIn('customfield', data['data']['type'])

    def test_add_field_invalid_type(self):
        """Ensure error is thrown if the JSON object has invalid type."""

        with self.client:
            response = self.client.post(
                '/sis/v1/customfields',
                data=json.dumps({
                    "data": {
                        "type": "contact",
                        "attributes": {
                            "key": "test"
                        }
                    }
                }),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"customfield\".",
                      data['errors'][0]['detail'])

    def test_add_field_missing_data(self):
        """Ensure error is thrown if the JSON object
        has messing required data."""

        with self.client:
            response = self.client.post(
                '/sis/v1/customfields',
                data=json.dumps({
                    "data": {
                        "type": "customfield",
                        "attributes": {
                            "key": "test"
                        }
                    }
                }),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      data['errors'][0]['detail'])

    def test_add_field_invalid_json(self):
        """Ensure error is thrown if the JSON object invalid."""

        with self.client:
            response = self.client.post(
                '/sis/v1/customfields',
                data=json.dumps({}),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.",
                      data['errors'][0]['detail'])

    def test_add_field_invalid_data_key(self):
        """Ensure error is thrown if the JSON object
         has invalid data key."""

        with self.client:
            response = self.client.post(
                '/sis/v1/customfields',
                data=json.dumps({
                    "data": {
                        "type": "customfield",
                        "attributes": {
                            "key": 123,
                            "value": "test"
                        }
                    }
                }),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Not a valid string.",
                      data['errors'][0]['detail'])


if __name__ == '__main__':
    unittest.main()
