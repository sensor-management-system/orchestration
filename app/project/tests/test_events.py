import json
import unittest

from project.api.models.event import Event
from project.api.schemas.event_schema import EventSchema
from project.tests.base import BaseTestCase


class TestEventServices(BaseTestCase):
    """
    Test Event Services
    """
    event_url = '/events'
    object_type = 'event'

    def test_get_devices(self):
        """Ensure the /event route behaves correctly."""
        response = self.client.get('/rdm/svm-api/v1/events')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, data['meta']['count'])
        # super().tear_down()

    def test_add_event_model(self):
        """""Ensure Add platform model """
        event = Event(id=145, description='test issued')
        EventSchema().dump(event)

    def test_add_event(self):
        """Ensure a new event can be added to the database."""
        event_data = {
            "data": {
                "type": "event",
                "attributes": {
                    "description": "test",
                }
            }
        }
        super().add_object(
            url=self.event_url, data_object=event_data,
            object_type=self.object_type)

    def test_add_event_invalid_type(self):
        """Ensure error is thrown if the JSON object has invalid type."""
        event_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "description": "test"
                }
            }
        }
        with self.client:
            data, response = super().prepare_response(
                url=self.event_url, data_object=event_data)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"event\".",
                      data['errors'][0]['detail'])

    def test_add_event_missing_data(self):
        """Ensure error is thrown if the JSON object
         has messing required data."""
        event_data = {
            "data": {
                "type": "event",
                "attributes": {

                }
            }
        }

        data, response = super().prepare_response(
            url=self.event_url, data_object=event_data)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      data['errors'][0]['detail'])

    def test_add_event_invalid_json(self):
        """Ensure error is thrown if the JSON object invalid."""
        event_data = {}

        data, response = super().prepare_response(
            url=self.event_url, data_object=event_data)
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.",
                      data['errors'][0]['detail'])

    def test_add_event_invalid_data_key(self):
        event_data = {
            "data": {
                "type": "event",
                "attributes": {
                    "description": 123
                }
            }
        }
        super().add_object_invalid_data_key(
            url=self.event_url, data_object=event_data)

        if __name__ == '__main__':
            unittest.main()
