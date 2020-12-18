import json
import unittest

from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.schemas.device_schema import DeviceSchema
from project.tests.base import BaseTestCase
from project.tests.read_from_json import extract_data_from_json_file
from project.tests.test_contacts import TestContactServices
from project.urls import base_url


class TestDeviceService(BaseTestCase):
    """Tests for the Device Service."""

    device_url = base_url + "/devices"
    object_type = "device"
    json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"

    def test_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get(base_url + "/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello Sensor!", data["message"])
        self.assertIn("success", data["status"])

    def test_get_devices(self):
        """Ensure the GET /devices route behaves correctly."""
        response = self.client.get(self.device_url)
        self.assertEqual(response.status_code, 200)

    def test_add_device_model(self):
        """""Ensure Add device model """
        sensor = Device(
            id=22,
            short_name="device_short_name test",
            description="device_description test",
            long_name="device_long_name test",
            manufacturer_name="manufacturer_name test",
            manufacturer_uri="http://cv/manufacturer_uri",
            model="device_model test",
            dual_use=True,
            serial_number="device_serial_number test",
            website="http://website/device",
            inventory_number="inventory_number test",
            persistent_identifier="persistent_identifier_test",
        )
        DeviceSchema().dump(sensor)
        db.session.add(sensor)
        db.session.commit()

        device = db.session.query(Device).filter_by(id=sensor.id).one()
        self.assertIn(device.model, sensor.model)

    def test_add_device(self):
        """Ensure a new device can be added to the database."""
        devices_json = extract_data_from_json_file(self.json_data_url, "devices")

        device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
        super().add_object(
            url=self.device_url, data_object=device_data, object_type=self.object_type
        )

    def add_device_contacts_relationship(self):
        """Ensure a new relationship between a device and a contact
        can be established.
        """
        contact = TestContactServices().test_add_contact()
        devices_json = extract_data_from_json_file(self.json_data_url, "devices")

        device_data = {
            "data": {"type": "device", "attributes": devices_json[0]},
            "relationships": {"data": [{"type": "contact", "id": contact.id}]},
        }
        data = super().add_object(
            url=self.device_url + "?include=contacts",
            data_object=device_data,
            object_type=self.object_type,
        )

        self.assertIn(
            contact.id, data["data"]["relationships"]["contacts"]["data"]["id"]
        )


if __name__ == "__main__":
    unittest.main()
