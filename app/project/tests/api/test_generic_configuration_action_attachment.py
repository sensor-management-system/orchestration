import json

from project import base_url
from project.tests.base import BaseTestCase
from project.tests.models.test_generic_action_attachment_model import (
    add_generic_configuration_action_attachment_model,
)


class TestGenericConfigurationActionAttachment(BaseTestCase):
    """Tests for the GenericConfigurationActionAttachment endpoints."""

    generic_configuration_action_attachment_url = (
        base_url + "/generic-configuration-action-attachments"
    )
    object_type = "generic_configuration_action_attachment"

    def test_get_generic_configuration_action_attachment(self):
        """Ensure the GET /generic_configuration_action_attachments route reachable."""
        response = self.client.get(self.generic_configuration_action_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_configuration_action_attachment_collection(self):
        """Test retrieve a collection of GenericConfigurationActionAttachment objects"""
        _ = add_generic_configuration_action_attachment_model()
        with self.client:
            response = self.client.get(self.generic_configuration_action_attachment_url)
        _ = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_post_generic_configuration_action_attachment(self):
        """Create GenericConfigurationActionAttachment"""

    def test_update_generic_configuration_action_attachment(self):
        """Update GenericConfigurationActionAttachment"""

    def test_delete_generic_configuration_action_attachment(self):
        """Delete GenericConfigurationActionAttachment """
        gca_a = add_generic_configuration_action_attachment_model()
        _ = super().delete_object(
            url=f"{self.generic_configuration_action_attachment_url}/{gca_a.id}",
        )
