import json
import unittest

from project.api.models.event import Event
from project.api.schemas.event_schema import EventSchema
from project.tests.base import BaseTestCase


class TestEventServices(BaseTestCase):
    """
    Test Event Services
    """
    url = '/sis/v1/events'
    object_type = 'event'

    def test_get_devices(self):
        """Ensure the /event route behaves correctly."""
        response = self.client.get('/sis/v1/events')
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
        data_object = {
            "data": {
                "type": "event",
                "attributes": {
                    "description": "test",
                }
            }
        }
        super(TestEventServices, self). \
            test_add_object(url=self.url,
                            data_object=data_object,
                            object_type=self.object_type)

    def test_add_event_invalid_type(self):
        """Ensure error is thrown if the JSON object has invalid type."""
        data_object = {
            "data": {
                "type": "platform",
                "attributes": {
                    "description": "test"
                }
            }
        }
        with self.client:
            data, response = super(TestEventServices, self).prepare_response(
                url=self.url, data_object=data_object)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"event\".",
                      data['errors'][0]['detail'])

    def test_add_event_missing_data(self):
        """Ensure error is thrown if the JSON object
         has messing required data."""
        data_object = {
            "data": {
                "type": "event",
                "attributes": {

                }
            }
        }
        with self.client:
            data, response = super(TestEventServices, self).prepare_response(
                url=self.url, data_object=data_object)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      data['errors'][0]['detail'])

    def test_add_event_invalid_json(self):
        """Ensure error is thrown if the JSON object invalid."""
        data_object = {}
        with self.client:
            data, response = super(TestEventServices, self).prepare_response(
                url=self.url, data_object=data_object)
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.",
                      data['errors'][0]['detail'])

    def test_add_event_invalid_data_key(self):
        data_object = {
            "data": {
                "type": "event",
                "attributes": {
                    "description": 123
                }
            }
        }
        with self.client:
            data, response = super(TestEventServices, self).prepare_response(
                url=self.url, data_object=data_object)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Not a valid string.",
                      data['errors'][0]['detail'])

        if __name__ == '__main__':
            unittest.main()
