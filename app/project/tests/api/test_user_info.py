import json
from unittest.mock import patch

from flask import current_app

from project import base_url
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


class TestUserinfo(BaseTestCase):
    """Tests for the Device Service."""

    url = base_url + "/user-info"

    def test_get_without_jwt(self):
        """Ensure the GET /user-info route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get_with_jwt_user_not_assigned_to_any_permission_group(self):
        """Ensure response with an empty list if user not assigned to any permission group"""
        access_headers = create_token()
        if current_app.config["IDL_URL"] is not None:
            response = self.client.get(self.url, headers=access_headers)
            self.assertEqual(response.status_code, 200)
            data = response.json["data"]
            self.assertEqual(data["attributes"]["admin"], [])
            self.assertEqual(data["attributes"]["member"], [])
        else:
            pass

    def test_get_with_jwt_user_is_assigned_to_permission_groups(self):
        """Ensure response with an empty list if user not assigned to any permission group"""
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.get(
                    f"{self.url}?include=device,contact,parent_platform,configuration",
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        self.assertEqual(data["attributes"]["admin"], ["1"])
        self.assertEqual(data["attributes"]["member"], ["2", "3"])

    def test_post_not_allowed(self):
        """Ensure post request not allowed."""
        access_headers = create_token()
        data = {}
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    self.url,
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
        self.assertEqual(response.status_code, 405)
        data = response.json
        self.assertEqual(data["errors"][0]["source"], "endpoint is readonly")
