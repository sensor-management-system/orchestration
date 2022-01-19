"""Tests for the generic platform action api."""

from project import base_url, db
from project.api.models import GenericPlatformAction
from project.tests.base import BaseTestCase
from project.tests.base import create_token

from project.tests.models.test_generic_actions_models import (
    generate_platform_action_model,
)


class TestGenericPlatformActionPermissions(BaseTestCase):
    """Tests for the GenericPlatformAction permissions."""

    url = base_url + "/generic-platform-actions"
    object_type = "generic_platform_action"

    def test_a_public_generic_platform_action(self):
        """Ensure a public generic platform action will be listed."""
        generic_device_action = generate_platform_action_model()
        action = (
            db.session.query(GenericPlatformAction)
            .filter_by(id=generic_device_action.id)
            .one()
        )
        self.assertEqual(action.description, generic_device_action.description)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_an_internal_generic_platform_action(self):
        """Ensure a public generic platform action won't be listed unless user provide a valid JWT."""
        generic_device_action = generate_platform_action_model(
            public=False, private=False, internal=True
        )
        action = (
            db.session.query(GenericPlatformAction)
            .filter_by(id=generic_device_action.id)
            .one()
        )
        self.assertEqual(action.description, generic_device_action.description)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
