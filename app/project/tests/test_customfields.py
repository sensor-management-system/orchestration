import unittest

from project.api.models.customfield import CustomField
from project.api.schemas.customfield_schema import CustomFieldSchema
from project.tests.base import BaseTestCase


class TestFieldServices(BaseTestCase):
    """
    Test Field Services
    """
    url = '/sis/v1/customfields'
    object_type = 'customfield'

    def test_add_attachment_model(self):
        """""Ensure Add an Field model """
        customfield = CustomField(id=5, key='test',
                                  value="test")
        CustomFieldSchema().dump(customfield)

    def test_add_field(self):
        """Ensure a new Field can be added to the database."""

        data_object = {
            "data": {
                "type": "customfield",
                "attributes": {
                    "key": "testKey1",
                    "value": "testVal1"
                }
            }
        }
        super(TestFieldServices, self). \
            test_add_object(url=self.url,
                            data_object=data_object,
                            object_type=self.object_type)

    def test_add_field_invalid_type(self):
        """Ensure error is thrown if the JSON object has invalid type."""

        data_object = {
            "data": {
                "type": "contact",
                "attributes": {
                    "key": "test"
                }
            }
        }
        with self.client:
            data, response = super(TestFieldServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"customfield\".",
                      data['errors'][0]['detail'])

    def test_add_field_missing_data(self):
        """Ensure error is thrown if the JSON object
        has messing required data."""

        data_object = {
            "data": {
                "type": "customfield",
                "attributes": {
                    "key": "test"
                }
            }
        }
        with self.client:
            data, response = super(TestFieldServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      data['errors'][0]['detail'])

    def test_add_field_invalid_json(self):
        """Ensure error is thrown if the JSON object invalid."""

        data_object = {}
        with self.client:
            data, response = super(TestFieldServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.",
                      data['errors'][0]['detail'])

    def test_add_field_invalid_data_key(self):
        """Ensure error is thrown if the JSON object
         has invalid data key."""

        data_object = {
            "data": {
                "type": "customfield",
                "attributes": {
                    "key": 123,
                    "value": "test"
                }
            }
        }
        with self.client:
            data, response = super(TestFieldServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Not a valid string.",
                      data['errors'][0]['detail'])


if __name__ == '__main__':
    unittest.main()
