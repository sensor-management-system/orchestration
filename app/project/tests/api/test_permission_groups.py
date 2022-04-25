from flask import current_app
from project import base_url
from project.tests.base import BaseTestCase
from project.tests.base import create_token


class TestPermissionGroup(BaseTestCase):
    """Tests for the Permission Group Service."""

    url = base_url + "/permission-groups"

    def test_get(self):
        """Ensure it works with a valid jwt."""
        if current_app.config['IDL_URL'] is not None:
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)
            data = response.json["data"]
            self.assertNotEqual(len(data), 0)
        else:
            pass
