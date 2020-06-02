import unittest

from project.api.models.customfield import CustomField
from project.api.schemas.customfield_schema import CustomFieldSchema
from project.tests.base import BaseTestCase


class TestFieldServices(BaseTestCase):
    """
    Test Field Services
    """
    field_url = '/customfields'
    object_type = 'customfield'

    def test_add_attachment_model(self):
        """""Ensure Add an Field model """
        customfield = CustomField(id=5, key='test',
                                  value="test")
        CustomFieldSchema().dump(customfield)

    def test_add_field(self):
        """Ensure a new Field can be added to the database."""

        c_field_data = {
            "data": {
                "type": "customfield",
                "attributes": {
                    "key": "testKey1",
                    "value": "testVal1"
                }
            }
        }
        super(). \
            add_object(url=self.field_url,
                       data_object=c_field_data,
                       object_type=self.object_type)

    def test_add_field_invalid_type(self):
        """Ensure error is thrown if the JSON object has invalid type."""

        c_field_data = {
            "data": {
                "type": "contact",
                "attributes": {
                    "key": "test"
                }
            }
        }

        data, response = super(). \
            prepare_response(url=self.field_url,
                             data_object=c_field_data)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"customfield\".",
                      data['errors'][0]['detail'])

    def test_add_field_missing_data(self):
        """Ensure error is thrown if the JSON object
        has messing required data."""

        c_field_data = {
            "data": {
                "type": "customfield",
                "attributes": {
                    "key": "test"
                }
            }
        }

        data, response = super(). \
            prepare_response(url=self.field_url,
                             data_object=c_field_data)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      data['errors'][0]['detail'])

    def test_add_field_invalid_json(self):
        """Ensure error is thrown if the JSON object invalid."""

        c_field_data = {}

        data, response = super(TestFieldServices, self). \
            prepare_response(url=self.field_url,
                             data_object=c_field_data)
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.",
                      data['errors'][0]['detail'])

    def test_add_field_invalid_data_key(self):
        """Ensure error is thrown if the JSON object
         has invalid data key."""

        c_field_data = {
            "data": {
                "type": "customfield",
                "attributes": {
                    "key": 123,
                    "value": "test"
                }
            }
        }

        super().add_object_invalid_data_key(
            url=self.attachment_url, data_object=c_field_data)


if __name__ == '__main__':
    unittest.main()
