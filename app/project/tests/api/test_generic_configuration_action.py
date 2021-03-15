import json
import os

from project import base_url
from project.api.models import Contact
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data, test_file_path
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_generic_actions_models import (
    generate_configuration_action_model,
)


class TestGenericConfigurationAction(BaseTestCase):
    """Tests for the GenericConfigurationAction endpoints."""

    url = base_url + "/generic-configuration-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
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
        """Ensure the GET /generic_configuration_actions route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_configuration_action_collection(self):
        """Test retrieve a collection of GenericConfigurationAction objects"""
        configuration_action = generate_configuration_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            configuration_action.description,
            data["data"][0]["attributes"]["description"],
        )

    def test_post_generic_configuration_action(self):
        """Create GenericConfigurationAction"""
        configuration = generate_configuration_model()
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        db.session.add_all([configuration, contact])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "Test GenericConfigurationAction",
                    "action_type_name": fake.pystr(),
                    "action_type_uri": fake.uri(),
                    "begin_date": fake.future_datetime().__str__(),
                    "end_date": fake.future_datetime().__str__(),
                },
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=configuration,contact",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_generic_configuration_action(self):
        """Update GenericConfigurationAction"""
        configuration_action = generate_configuration_action_model()
        gca_updated = {
            "data": {
                "type": self.object_type,
                "id": configuration_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{configuration_action.id}",
            data_object=gca_updated,
            object_type=self.object_type,
        )

    def test_delete_generic_configuration_action(self):
        """Delete GenericConfigurationAction """
        configuration_action = generate_configuration_action_model()
        _ = super().delete_object(
            url=f"{self.url}/{configuration_action.id}",
        )
