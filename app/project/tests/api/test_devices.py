from project import base_url
from project.api.models import Contact
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, generate_token_data
from project.tests.read_from_json import extract_data_from_json_file


class TestDeviceService(BaseTestCase):
    """Tests for the Device Service."""

    device_url = base_url + "/devices"
    object_type = "device"
    json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"

    def test_get_devices(self):
        """Ensure the GET /devices route behaves correctly."""
        response = self.client.get(self.device_url)
        self.assertEqual(response.status_code, 200)

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
        jwt = generate_token_data()
        contact = Contact(
            given_name=jwt["given_name"],
            family_name=jwt["family_name"],
            email=jwt["email"],
        )
        db.session.add(contact)
        db.session.commit()
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
