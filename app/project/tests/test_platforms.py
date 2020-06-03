import json
import unittest

from project.api.models.platform import Platform
from project.api.schemas.platform_schema import PlatformSchema
from project.tests.base import BaseTestCase


class TestPlatformServices(BaseTestCase):
    """
    Test Event Services
    """
    url = '/sis/v1/platforms'

    def test_get_platfoms(self):
        """Ensure the /platform route behaves correctly."""
        response = self.client.get('/sis/v1/platforms')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("http://localhost/sis/v1/platforms",
                      data['links']['self'])

    def test_add_platform_model(self):
        """""Ensure Add platform model """
        platform = Platform(id=13,
                            short_name='short', type="type")
        PlatformSchema().dump(platform)

    def test_add_platform(self):
        """Ensure a new platform can be added to the database."""

        data_object = {
            "data": {
                "type": "platform",
                "attributes": {
                    "longName": "testLong",
                    "platform_type": "testPlType",
                    "short_name": "short",
                    "description": "string",
                    "manufacturer": "string",
                    "type": "type",
                    "inventory_number": 12,
                    "configuration_date": "2020-05-04 11",
                    "url": "string"
                }
            }
        }
        with self.client:
            data, response = super(TestPlatformServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

            self.assertEqual(response.status_code, 201)
            self.assertIn('TYPE_SHORT', data['data']['attributes']['urn'])
            self.assertIn('platform', data['data']['type'])

    def test_add_platform_invalid_type(self):
        """Ensure error is thrown if the platform object has invalid type."""

        data_object = {
            "data": {
                "type": "device",
                "attributes": {
                    "type": "TYPE"
                }
            }
        }
        with self.client:
            data, response = super(TestPlatformServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"platform\".",
                      data['errors'][0]['detail'])

    def test_add_platform_missing_data(self):
        """Ensure error is thrown if the platform object
        has messing required data."""

        data_object = {
            "data": {
                "type": "platform",
                "attributes": {
                    "type": "test",
                }
            }
        }

        with self.client:
            data, response = super(TestPlatformServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      data['errors'][0]['detail'])

    def test_add_platform_invalid_json(self):
        """Ensure error is thrown if the platform object invalid."""

        data_object = {}

        with self.client:
            data, response = super(TestPlatformServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.",
                      data['errors'][0]['detail'])

    def test_add_platform_invalid_data_key(self):
        """Ensure error is thrown if the platform object
         has invalid data key."""

        data_object = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": "short",
                    "type": 123
                }
            }
        }

        with self.client:
            data, response = super(TestPlatformServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Not a valid string.",
                      data['errors'][0]['detail'])

    def test_get_platforms_via_id(self):
        """Ensure the get /platform/<id> route behaves correctly."""
        response = self.client.get('/sis/v1/platforms/1')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('TYPE_SHORT', data['data']['attributes']['urn'])

    def test_patch_platforms_via_id(self):
        """Ensure the patch /platform/<id> route behaves correctly."""
        data_object = {
            "data": {
                "type": "platform",
                "id": 1,
                "attributes": {
                    "short_name": "new"
                }
            }
        }

        with self.client:
            data, response = super(TestPlatformServices, self). \
                prepare_response(url=self.url,
                                 data_object=data_object)

        self.assertEqual(response.status_code, 200)
        self.assertIn('TYPE_NEW', data['data']['attributes']['urn'])

    def test_z_platform_delete(self):
        """Ensure the  delete /platform/<id> route behaves correctly."""
        response = self.client.delete('/sis/v1/platforms/1')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Object successfully deleted', data['meta']['message'])
        super().tear_down()

    def test_get_platform_devices_via_id(self):
        """Ensure the get devices attached to a platform
         /platform/<id> route behaves correctly."""
        response = self.client.get('/sis/v1/platforms/1/relationships/devices')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('/sis/v1/platforms/1/relationships/device',
                      data['links']['self'])

    def test_post_relationship_platform_devices_via_id(self):
        """Ensure the post relationship between a
         devices and a platform
         /platform/<id> route behaves correctly."""
        data_object = {
            "data": [
                {
                    "type": "device",
                    "id": "1"
                }
            ]
        }

        with self.client:
            data, response = super().prepare_response(
                url='/sis/v1/platforms/1/relationships/devices',
                data_object=data_object)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Relationship successfully created',
                      data['meta']['message'])


if __name__ == '__main__':
    unittest.main()
