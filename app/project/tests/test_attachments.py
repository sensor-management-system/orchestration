import json
import unittest

from project.api.models.attachment import Attachment
from project.api.schemas.attachment_schema import AttachmentSchema
from project.tests.base import BaseTestCase


class TestAttachmentServices(BaseTestCase):
    """
    Test Attachment class
    """
    attachment_url = '/rdm/svm-api/v1/attachments'
    object_type = 'attachment'

    def test_add_attachment_model(self):
        """""Ensure Add an Attachment model """
        attachment = Attachment(id=45, label='test',
                                url="http://test.test")
        AttachmentSchema().dump(attachment)

    def test_add_attachment(self):
        """Ensure a new Attachment can be added to the database."""

        attachment_data = {
            "data": {
                "type": "attachment",
                "attributes": {
                    "label": "test2",
                    "url": "http://test.test"
                }
            }
        }
        super(). \
            add_object(url=self.attachment_url,
                       data_object=attachment_data,
                       object_type=self.object_type)

    def test_add_attachment_invalid_type(self):
        """Ensure error is thrown if the JSON object has invalid type."""

        attachment_data = {
            "data": {
                "type": "contact",
                "attributes": {
                    "url": "test"
                }
            }
        }

        data, response = super().prepare_response(
            url=self.attachment_url, data_object=attachment_data)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"attachment\".",
                      data['errors'][0]['detail'])

    def test_add_attachment_missing_data(self):
        """Ensure error is thrown if the JSON object
        has messing required data."""
        attachment_data = {
            "data": {
                "type": "attachment",
                "attributes": {
                    "label": "test3"
                }
            }
        }

        data, response = super().prepare_response(
            url=self.attachment_url, data_object=attachment_data)

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      data['errors'][0]['detail'])

    def test_add_attachment_invalid_json(self):
        """Ensure error is thrown if the JSON
        object invalid."""

        attachment_data = {}
        with self.client:
            data, response = super(). \
                prepare_response(url=self.attachment_url,
                                 data_object=attachment_data)
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.",
                      data['errors'][0]['detail'])

    def test_add_attachment_invalid_data_key(self):
        """Ensure error is thrown if the JSON object
         has invalid data key."""

        attachment_data = {
            "data": {
                "type": "attachment",
                "attributes": {
                    "url": 123
                }
            }
        }
        super().add_object_invalid_data_key(
            url=self.attachment_url, data_object=attachment_data)


if __name__ == '__main__':
    unittest.main()
