# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Test cases for checking the remove slash middleware."""


from project import base_url
from project.api.models import Device
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestRemoveSlashMiddleware(BaseTestCase):
    """Test class for the remove slash middlware."""

    def test_with_slash(self):
        """Ensure that a simple use case works also if there is a slash at the end."""
        url = f"{base_url}/devices/"

        response_direct = self.client.get(url)
        self.assertEqual(response_direct.status_code, 302)

        redirected_url = response_direct.headers["location"]
        self.assertEqual(redirected_url, f"{base_url}/devices")

        response_redirected = self.client.get(redirected_url)
        self.assertEqual(response_redirected.status_code, 200)

    def test_with_slash_and_query_parameters(self):
        """Ensure it works with query parameters too."""
        device1 = Device(
            short_name="zero test device",
            is_public=True,
            is_internal=False,
            archived=False,
        )
        device2 = Device(
            short_name="first test device",
            is_public=True,
            is_internal=False,
            archived=True,
        )

        db.session.add_all([device1, device2])
        db.session.commit()

        url = f"{base_url}/devices/"
        params = {"hide_archived": "false", "sort": "short_name"}

        response_direct = self.client.get(url, query_string=params)
        self.assertEqual(response_direct.status_code, 302)

        redirected_url = response_direct.headers["location"]
        self.assertEqual(
            redirected_url, f"{base_url}/devices?hide_archived=false&sort=short_name"
        )

        response_redirected = self.client.get(redirected_url)
        self.assertEqual(response_redirected.status_code, 200)

        data = response_redirected.json["data"]
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["attributes"]["short_name"], "first test device")
        self.assertEqual(data[1]["attributes"]["short_name"], "zero test device")
