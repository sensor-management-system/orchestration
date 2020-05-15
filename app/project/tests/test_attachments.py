import json
import unittest

from project.api.models.attachment import Attachment
from project.api.schemas.attachmentSchema import AttachmentSchema
from project.tests.base import BaseTestCase


class TestAttachmentServices(BaseTestCase):

    def test_add_attachment_model(self):
        """""Ensure Add an Attachment model """
        attachment = Attachment(id=45, label='test',
                                url="http://test.test")
        AttachmentSchema().dump(attachment)

    def test_add_attachment(self):
        """Ensure a new Attachment can be added to the database."""
        super().create_app()
        super().set_up()

        with self.client:
            response = self.client.post(
                '/sis/v1/attachments',
                data=json.dumps({
                    "data": {
                        "type": "attachment",
                        "attributes": {
                            "label": "test2",
                            "url": "http://test.test"
                        }
                    }
                }),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('test', data['data']['attributes']['label'])
        self.assertIn('attachment', data['data']['type'])

    def test_add_attachment_invalid_type(self):
        """Ensure error is thrown if the JSON object has invalid type."""

        with self.client:
            response = self.client.post(
                '/sis/v1/attachments',
                data=json.dumps({
                    "data": {
                        "type": "contact",
                        "attributes": {
                            "url": "test"
                        }
                    }
                }),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"attachment\".",
                      data['errors'][0]['detail'])

    def test_add_attachment_missing_data(self):
        """Ensure error is thrown if the JSON object
        has messing required data."""

        with self.client:
            response = self.client.post(
                '/sis/v1/attachments',
                data=json.dumps({
                    "data": {
                        "type": "attachment",
                        "attributes": {
                            "label": "test3"
                        }
                    }
                }),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      data['errors'][0]['detail'])

    def test_add_attachment_invalid_json(self):
        """Ensure error is thrown if the JSON object invalid."""

        with self.client:
            response = self.client.post(
                '/sis/v1/attachments',
                data=json.dumps({}),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.",
                      data['errors'][0]['detail'])

    def test_add_attachment_invalid_data_key(self):
        """Ensure error is thrown if the JSON object
         has invalid data key."""

        with self.client:
            response = self.client.post(
                '/sis/v1/attachments',
                data=json.dumps({
                    "data": {
                        "type": "attachment",
                        "attributes": {
                            "url": 123
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
