import os
from datetime import datetime

from project import base_url
from project.tests.base import BaseTestCase, fake, generate_token_data, test_file_path
from project.tests.read_from_json import extract_data_from_json_file


class TestGenericConfigurationActionServices(BaseTestCase):
    """Tests for the GenericConfigurationAction endpoints."""

    url = base_url + "/generic-configuration-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    configurations_url = base_url + "/configurations"
    object_type = "generic_configuration_action"

    json_data_url = os.path.join(
        test_file_path, "drafts", "configurations_test_data.json"
    )
    device_json_data_url = os.path.join(
        test_file_path, "drafts", "devices_test_data.json"
    )
    platform_json_data_url = os.path.join(
        test_file_path, "drafts", "platforms_test_data.json"
    )

    def test_get_generic_configuration_action(self):
        """Ensure the List /generic_configuration_action route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_add_generic_configuration_action(self):
        """
        Ensure POST a new generic config
        action can be added to the database.
        """
        data = self.make_generic_configuration_action_data()

        _ = super().add_object(
            url=f"{self.url}?include=configuration,contact",
            data_object=data,
            object_type=self.object_type,
        )

    def make_generic_configuration_action_data(self):
        devices_json = extract_data_from_json_file(self.device_json_data_url, "devices")
        device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
        device = super().add_object(
            url=self.device_url, data_object=device_data, object_type="device"
        )
        platforms_json = extract_data_from_json_file(
            self.platform_json_data_url, "platforms"
        )
        platform_data = {"data": {"type": "platform", "attributes": platforms_json[0]}}
        super().add_object(
            url=self.platform_url, data_object=platform_data, object_type="platform"
        )
        config_json = extract_data_from_json_file(self.json_data_url, "configuration")
        config_data = {"data": {"type": "configuration", "attributes": config_json[0]}}
        super().add_object(
            url=self.configurations_url,
            data_object=config_data,
            object_type="configuration",
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
                    "configuration": {
                        "data": {"type": "configuration", "id": device["data"]["id"]}
                    },
                    "contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }
        return data

    def test_update_generic_configuration_action(self):
        """Ensure a generic_configuration_action can be updateded."""
        old_generic_configuration_action_data = (
            self.make_generic_configuration_action_data()
        )
        old_generic_configuration_action = super().add_object(
            url=f"{self.url}?include=configuration,contact",
            data_object=old_generic_configuration_action_data,
            object_type=self.object_type,
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
        new_data = {
            "data": {
                "type": self.object_type,
                "id": old_generic_configuration_action["data"]["id"],
                "attributes": {
                    "description": fake.paragraph(nb_sentences=2),
                    "action_type_name": fake.lexify(
                        text="Random type: ??????????", letters="ABCDE"
                    ),
                    "action_type_uri": fake.uri(),
                    "begin_date": datetime.now().__str__(),
                },
                "relationships": {
                    "configuration": {"data": {"type": "configuration", "id": "1"}},
                    "contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }
        old_id = old_generic_configuration_action["data"]["id"]

        _ = super().update_object(
            url=f"{self.url}/{old_id}?include=configuration,contact",
            data_object=new_data,
            object_type=self.object_type,
        )

    def test_delete_generic_configuration_action(self):
        """Ensure a generic_configuration_action can be deleted"""

        generic_configuration_action_data = (
            self.make_generic_configuration_action_data()
        )

        generic_configuration_action = super().add_object(
            url=f"{self.url}?include=configuration,contact",
            data_object=generic_configuration_action_data,
            object_type=self.object_type,
        )
        _ = super().delete_object(
            url=f"{self.url}/{generic_configuration_action['data']['id']}",
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
