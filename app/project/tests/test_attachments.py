import json
import unittest

from project.api.models.attachment import Attachment
from project.api.schemas.attachment_schema import AttachmentSchema
from project.tests.base import BaseTestCase


class TestAttachmentServices(BaseTestCase):
    """
    Test Attachment class
    """
    url = '/sis/v1/attachments'
    object_type = 'attachment'

    def test_add_attachment_model(self):
        """""Ensure Add an Attachment model """
        attachment = Attachment(id=45, label='test',
                                url="http://test.test")
        AttachmentSchema().dump(attachment)

    def test_add_attachment(self):
        """Ensure a new Attachment can be added to the database."""
        super().create_app()
        super().set_up()

        data_object = {
            "data": {
                "type": "attachment",
                "attributes": {
                    "label": "test2",
                    "url": "http://test.test"
                }
            }
        }
        super(TestAttachmentServices, self). \
            test_add_object(url=self.url,
                            data_object=data_object,
                            object_type=self.object_type)

    def test_add_attachment_invalid_type(self):
        """Ensure error is thrown if the JSON object has invalid type."""

        data_object = {
            "data": {
                "type": "contact",
                "attributes": {
                    "url": "test"
                }
            }
        }
        with self.client:
            data, response = super(TestAttachmentServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"attachment\".",
                      data['errors'][0]['detail'])

    def test_add_attachment_missing_data(self):
        """Ensure error is thrown if the JSON object
        has messing required data."""
        data_object = {
            "data": {
                "type": "attachment",
                "attributes": {
                    "label": "test3"
                }
            }
        }
        with self.client:
            data, response = super(TestAttachmentServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      data['errors'][0]['detail'])

    def test_add_attachment_invalid_json(self):
        """Ensure error is thrown if the JSON
        object invalid."""

        data_object = {}
        with self.client:
            data, response = super(TestAttachmentServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.",
                      data['errors'][0]['detail'])

    def test_add_attachment_invalid_data_key(self):
        """Ensure error is thrown if the JSON object
         has invalid data key."""

        data_object = {
            "data": {
                "type": "attachment",
                "attributes": {
                    "url": 123
                }
            }
        }
        with self.client:
            data, response = super(TestAttachmentServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Not a valid string.",
                      data['errors'][0]['detail'])


if __name__ == '__main__':
    unittest.main()
