"""Tests for the platform software update actions api."""
import json

from project import base_url, db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data
from project.tests.base import create_token
from project.tests.models.test_software_update_actions_model import (
    add_platform_software_update_action_model,
)


class TestPlatformSoftwareUpdateAction(BaseTestCase):
    """Tests for the PlatformSoftwareUpdateAction endpoints."""

    url = base_url + "/platform-software-update-actions"
    object_type = "platform_software_update_action"

    def test_get_platform_software_update_action_collection(self):
        """Test retrieve a collection of public PlatformSoftwareUpdateAction objects."""
        sau = add_platform_software_update_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(sau.description, data["data"][0]["attributes"]["description"])

    def test_get_internal_platform_software_update_action_collection(self):
        """Test retrieve a collection of internal PlatformSoftwareUpdateAction objects."""
        _ = add_platform_software_update_action_model(
            public=False, private=False, internal=True
        )
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
