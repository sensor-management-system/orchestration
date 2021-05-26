import json

from project import base_url
from project.tests.base import BaseTestCase


class HealthCheck(BaseTestCase):
    """Test whether the service is alive."""

    def test_ping(self):
        """Ensure the /ping can be reached."""
        response = self.client.get(base_url + "/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Pong", data["message"])
        self.assertIn("success", data["status"])
