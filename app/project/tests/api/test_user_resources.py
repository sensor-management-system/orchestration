import json

from project import base_url
from project.tests.base import BaseTestCase, create_token, fake
from project.tests.models.test_user_model import add_user


class TestUserServices(BaseTestCase):
    """
    Test User Services
    """

    url = base_url + "/users"
    object_type = "user"

    def test_get_users(self):
        """Ensure the /users route behaves correctly."""
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [])

    def test_get_collection_of_users(self):
        """Ensure contact get collection behaves correctly."""
        user = add_user()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.subject, data["data"][0]["attributes"]["subject"])

    def test_fail_post_a_contact_anonymous(self):
        """Ensure using post request will fail."""
        user = {
            "subject": fake.pystr(),
        }

        data = {"data": {"type": "user", "attributes": user}}
        with self.client:
            response = self.client.post(
                self.url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 401)

    def test_fail_post_a_contact_authentificated(self):
        """Ensure using post request will fail."""
        user = {
            "subject": fake.pystr(),
        }

        data = {"data": {"type": "user", "attributes": user}}
        with self.client:
            response = self.client.post(
                self.url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        self.assertEqual(response.status_code, 405)

    def test_fail_patch_a_contact_anonymous(self):
        """Ensure using patch request will fail."""

        user = add_user()
        user_data = {
            "data": {
                "type": "user",
                "id": user.id,
                "attributes": {"subject": "updated"},
            }
        }

        with self.client:
            response = self.client.patch(
                f"{self.url}/{user.id}",
                data=json.dumps(user_data),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 401)

    def test_fail_patch_a_contact_authentificated(self):
        """Ensure using patch request will fail."""

        user = add_user()
        user_data = {
            "data": {
                "type": "user",
                "id": user.id,
                "attributes": {"subject": "updated"},
            }
        }

        with self.client:
            response = self.client.patch(
                f"{self.url}/{user.id}",
                data=json.dumps(user_data),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        self.assertEqual(response.status_code, 405)

    def test_fail_delete_a_contact_anonymous(self):
        """Ensure using delete request will fail."""

        user = add_user()
        with self.client:
            response = self.client.delete(
                f"{self.url}/{user.id}",
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 401)

    def test_fail_delete_a_contact_authenticated(self):
        """Ensure using delete request will fail."""

        user = add_user()
        with self.client:
            response = self.client.delete(
                f"{self.url}/{user.id}",
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        self.assertEqual(response.status_code, 405)
