import json
import unittest

from project.api.models.device import Device
from project.api.schemas.device_schema import DeviceSchema
from project.tests.base import BaseTestCase


class TestDeviceService(BaseTestCase):
    """Tests for the Device Service."""
    device_url = '/devices'

    def test_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/sis/v1/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello Sensor!', data['message'])
        self.assertIn('success', data['status'])
        # super().tear_down()

    def test_get_devices(self):
        """Ensure the GET /devices route behaves correctly."""
        response = self.client.get('/sis/v1/devices')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("http://localhost/sis/v1/devices",
                      data['links']['self'])

    def test_add_device_model(self):
        """""Ensure Add device model """
        sensor = Device(id=22, serial_number='123456789',
                        manufacturer="manufacturer",
                        model="model", inventory_number="123123",
                        persistent_identifier="456456", type="type")
        DeviceSchema().dump(sensor)

    def test_add_device(self):
        """Ensure a new device can be added to the database."""
        # super().create_app()
        # super().set_up()

        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "serial_number": "0125436987",
                    "manufacturer": "manufacturer",
                    "model": "model",
                    "inventory_number": "0001122",
                    "persistent_identifier": "54564654",
                    "type": "TYPE"
                }
            }
        }

        data, response = super(). \
            prepare_response(url=self.device_url,
                             data_object=device_data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('MANUFACTURER_MODEL_TYPE_125436987',
                      data['data']['attributes']['urn'])

    def test_add_device_invalid_type(self):
        """Ensure error is thrown if the JSON object has invalid type."""

        device_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "serial_number": "0125436987",
                    "manufacturer": "manufacturer",
                    "model": "model",
                    "inventory_number": "0001122",
                    "persistent_identifier": "54564654",
                    "type": "TYPE"
                }
            }
        }
        with self.client:
            data, response = super(). \
                prepare_response(url=self.device_url,
                                 data_object=device_data)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Invalid type. Expected \"device\".",
                      data['errors'][0]['detail'])

    def test_add_device_missing_data(self):
        """Ensure error is thrown if the JSON object
        has messing required data."""

        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "serial_number": "0125436987",
                }
            }
        }
        with self.client:
            data, response = super(). \
                prepare_response(url=self.device_url,
                                 data_object=device_data)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Missing data for required field.",
                      data['errors'][0]['detail'])

    def test_add_device_invalid_json(self):
        """Ensure error is thrown if the JSON object invalid."""

        device_data = {
            "data": {}
        }
        with self.client:
            data, response = super(). \
                prepare_response(url=self.device_url,
                                 data_object=device_data)
        self.assertEqual(response.status_code, 422)
        self.assertIn("Object must include `data` key.",
                      data['errors'][0]['detail'])

    def test_add_device_invalid_data_key(self):
        """Ensure error is thrown if the JSON object
         has invalid data key."""

        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "serial_number": "0125436987",
                    "manufacturer": "manufacturer",
                    "model": 123,
                    "inventory_number": "0001122",
                    "persistent_identifier": "54564654",
                    "type": "TYPE"
                }
            }
        }

        super().add_object_invalid_data_key(
            url=self.attachment_url, data_object=device_data)

    def test_patch_devices_via_id(self):
        """Ensure the patch /device/<id> route behaves correctly."""
        device_data = {
            "data": {
                "type": "device",
                "id": 1,
                "attributes": {
                    "model": "model_new"
                }
            }
        }

        data, response = super(). \
            prepare_response(url=self.device_url,
                             data_object=device_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('MANUFACTURER_MODEL_NEW_TYPE_125436987',
                      data['data']['attributes']['urn'])


if __name__ == '__main__':
    unittest.main()
