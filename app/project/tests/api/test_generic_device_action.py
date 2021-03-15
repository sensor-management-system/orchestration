import os
from datetime import datetime

from project import base_url
from project.tests.base import BaseTestCase, fake, generate_token_data, test_file_path
from project.tests.read_from_json import extract_data_from_json_file


class TestGenericDeviceAction(BaseTestCase):
    """Tests for the GenericDeviceAction endpoints."""

    url = base_url + "/generic-device-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "generic_device_action"
    json_data_url = os.path.join(test_file_path, "drafts", "configurations_test_data.json")
    device_json_data_url = os.path.join(test_file_path, "drafts", "devices_test_data.json")
    platform_json_data_url = os.path.join(test_file_path, "drafts", "platforms_test_data.json")

    def test_get_generic_device_action(self):
        """Ensure the GET /generic_device_action route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_add_generic_device_action(self):
        """
        Ensure POST a new generic device
        action can be added to the database.
        """
        data = self.make_generic_device_action_data()

        _ = super().add_object(
            url=f"{self.url}?include=device,contact",
            data_object=data,
            object_type=self.object_type,
        )

    def make_generic_device_action_data(self):
        devices_json = extract_data_from_json_file(self.device_json_data_url, "devices")
        device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
        device = super().add_object(
            url=self.device_url, data_object=device_data, object_type="device"
        )
        mock_jwt = generate_token_data()
        contact_data = {
            "data": {
                "type": "contact",
                "attributes": {
                    "given_name": mock_jwt["given_name"],
                    "family_name": mock_jwt["family_name"],
                    "email": mock_jwt["email"],
                    "website": fake.url(),
                },
            }
        }
        contact = super().add_object(
            url=self.contact_url, data_object=contact_data, object_type="contact"
        )
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": fake.paragraph(nb_sentences=3),
                    "action_type_name": fake.lexify(
                        text="Random type: ??????????", letters="ABCDE"
                    ),
                    "action_type_uri": fake.uri(),
                    "begin_date": datetime.now().__str__(),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device["data"]["id"]}},
                    "contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }
        return data

    def test_update_generic_device_action(self):
        """Ensure a generic_device_action can be updated."""
        generic_device_action_data = self.make_generic_device_action_data()
        generic_device_action = super().add_object(
            url=f"{self.url}?include=device,contact",
            data_object=generic_device_action_data,
            object_type=self.object_type,
        )
        mock_jwt = generate_token_data()
        contact_data1 = {
            "data": {
                "type": "contact",
                "attributes": {
                    "given_name": mock_jwt["given_name"],
                    "family_name": mock_jwt["family_name"],
                    "email": mock_jwt["email"],
                    "website": fake.url(),
                },
            }
        }
        contact = super().add_object(
            url=self.contact_url, data_object=contact_data1, object_type="contact"
        )
        new_data = {
            "data": {
                "type": self.object_type,
                "id": generic_device_action["data"]["id"],
                "attributes": {
                    "description": fake.paragraph(nb_sentences=3),
                    "action_type_name": fake.lexify(
                        text="Random type: ??????????", letters="ABCDE"
                    ),
                    "action_type_uri": fake.uri(),
                    "begin_date": datetime.now().__str__(),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": "1"}},
                    "contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{generic_device_action['data']['id']}?include=device,contact",
            data_object=new_data,
            object_type=self.object_type,
        )

    def test_delete_generic_device_action(self):
        """Ensure a generic_device_action can be deleted"""

        data = self.make_generic_device_action_data()

        obj = super().add_object(
            url=f"{self.url}?include=device,contact",
            data_object=data,
            object_type=self.object_type,
        )
        _ = super().delete_object(
            url=f"{self.url}/{obj['data']['id']}",
        )
