import json

from project import base_url
from project.tests.base import BaseTestCase

from project.tests.models.test_generic_actions_models import generate_configuration_action_model


class TestGenericConfigurationAction(BaseTestCase):
    """Tests for the GenericConfigurationAction endpoints."""

    generic_configuration_action_url = base_url + "/generic-configuration-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "generic_configuration_action"
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = (
        "/usr/src/app/project/tests/drafts/platforms_test_data.json"
    )

    def test_get_generic_configuration_action(self):
        """Ensure the GET /generic_configuration_actions route reachable."""
        response = self.client.get(self.generic_configuration_action_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_configuration_action_collection(self):
        """Test retrieve a collection of GenericConfigurationAction objects"""
        gca = generate_configuration_action_model()
        with self.client:
            response = self.client.get(self.generic_configuration_action_url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            gca.description,
            data["data"][0]["attributes"]["description"],
        )

    def test_post_generic_configuration_action(self):
        """Create GenericConfigurationAction"""
        pass

    def test_update_generic_configuration_action(self):
        """Update GenericConfigurationAction"""
        gca = generate_configuration_action_model()
        gca_updated = {
            "data": {
                "type": self.object_type,
                "id": gca.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.generic_configuration_action_url}/{gca.id}",
            data_object=gca_updated,
            object_type=self.object_type,
        )

    def test_delete_generic_configuration_action(self):
        """Delete GenericConfigurationAction """
        gca = generate_configuration_action_model()
        _ = super().delete_object(
            url=f"{self.generic_configuration_action_url}/{gca.id}",
        )
