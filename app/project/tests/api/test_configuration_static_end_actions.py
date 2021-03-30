import json

from project import base_url, db
from project.api.models import Contact
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_configuration_static_action_model import (
    add_static_location_end_action_model,
)
from project.tests.models.test_configurations_model import generate_configuration_model


class TestConfigurationStaticLocationEndActionServices(BaseTestCase):
    """Tests for the ConfigurationStaticLocationEndAction endpoint."""

    url = base_url + "/static-location-end-actions"
    contact_url = base_url + "/contacts"
    object_type = "configuration_static_location_end_action"

    def test_get_configuration_static_location_action(self):
        """Ensure the List /configuration_static_location_end_action route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_calibration_action_collection(self):
        """Test retrieve a collection of configuration_static_location_end_action objects."""
        static_location_end_action = add_static_location_end_action_model()
        print(f"d: {static_location_end_action.description}")
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            static_location_end_action.description,
            data["data"][0]["attributes"]["description"],
        )

    def test_add_configuration_static_end_location_action(self):
        """
        Ensure POST a new configuration static location end action
        can be added to the database.
        """
        config = generate_configuration_model()
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        db.session.add_all([contact, config])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "end_date": fake.future_datetime().__str__(),
                    "description": "test configuration_static_location_end_action",
                },
                "relationships": {
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "configuration": {
                        "data": {"type": "configuration", "id": config.id}
                    },
                },
            }
        }

        _ = super().add_object(
            url=f"{self.url}?include=configuration,contact",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_configuration_static_end_location_action(self):
        """Ensure a configuration_static_end_location_action can be updated."""
        static_location_end_action = add_static_location_end_action_model()
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
                "id": static_location_end_action.id,
                "attributes": {
                    "description": "changed",
                },
                "relationships": {
                    "contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }

        _ = super().update_object(
            url=f"{self.url}/{static_location_end_action.id}?include=contact",
            data_object=new_data,
            object_type=self.object_type,
        )

    def test_delete_configuration_static_end_location_action(self):
        """Ensure a configuration_static_end_location_action can be deleted"""

        static_location_end_action = add_static_location_end_action_model()

        _ = super().delete_object(
            url=f"{self.url}/{static_location_end_action.id}",
        )
