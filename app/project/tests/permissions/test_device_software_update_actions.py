"""Tests for the device software update action api."""

import json

from project import base_url
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.models.test_software_update_actions_model import (
    add_device_software_update_action_model,
)

from project.tests.base import create_token


class TestDeviceSoftwareUpdateAction(BaseTestCase):
    """Tests for the DeviceSoftwareUpdateAction endpoints."""

    url = base_url + "/device-software-update-actions"
    object_type = "device_software_update_action"

    def test_get_device_software_update_action_collection(self):
        """Test retrieve a collection of public DeviceSoftwareUpdateAction objects."""
        sau = add_device_software_update_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(sau.description, data["data"][0]["attributes"]["description"])

    def test_get_internal_device_software_update_action_collection(self):
        """Test retrieve a collection of internal DeviceSoftwareUpdateAction objects."""
        _ = add_device_software_update_action_model(
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
