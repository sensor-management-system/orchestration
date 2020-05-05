import json
import unittest


from project.api.models.event import Event
from project.api.schemas.eventSchema import EventSchema
from project.tests.base import BaseTestCase


class TestEventServices(BaseTestCase):
    def test_get_devices(self):
        """Ensure the /event route behaves correctly."""
        response = self.client.get('/sis/v1/events')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("http://localhost/sis/v1/events",
                      data['links']['self'])
        #super().tear_down()

    def test_add_platform_model(self):
        """""Ensure Add platform model """
        event = Event(id=145, description='test issued')
        EventSchema().dump(event)

    def test_add_event(self):
        """Ensure a new event can be added to the database."""

        with self.client:
            response = self.client.post(
                '/sis/v1/events',
                data=json.dumps({
                    "data": {
                        "type": "event",
                        "attributes": {
                            "description": "test",
                        }
                    }
                }),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('test', data['data']['attributes']['description'])
        self.assertIn('event', data['data']['type'])

    def test_add_event_invalid_type(self):
        """Ensure error is thrown if the JSON object has invalid type."""

        with self.client:
            response = self.client.post(
                '/sis/v1/events',
                data=json.dumps({
                    "data": {
                        "type": "platform",
                        "attributes": {
                            "description": "test"
                        }
                    }
                }),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"event\".", data['errors'][0]['detail'])

    def test_add_event_missing_data(self):
        """Ensure error is thrown if the JSON object has messing required data."""

        with self.client:
            response = self.client.post(
                '/sis/v1/events',
                data=json.dumps({
                    "data": {
                        "type": "event",
                        "attributes": {

                        }
                    }
                }),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.", data['errors'][0]['detail'])

    def test_add_event_invalid_json(self):
        """Ensure error is thrown if the JSON object invalid."""

        with self.client:
            response = self.client.post(
                '/sis/v1/events',
                data=json.dumps({}),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.", data['errors'][0]['detail'])

    def test_add_event_invalid_data_key(self):
        """Ensure error is thrown if the JSON object has invalid data key."""

        with self.client:
            response = self.client.post(
                '/sis/v1/events',
                data=json.dumps({
                     "data": {
                        "type": "event",
                        "attributes": {
                            "description": 123
                        }
                    }
                }),
                content_type='application/vnd.api+json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Not a valid string.", data['errors'][0]['detail'])


if __name__ == '__main__':
    unittest.main()
