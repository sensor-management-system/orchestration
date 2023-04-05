# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the openapi endpoints."""

from project import base_url
from project.tests.base import BaseTestCase


class TestOpenapiHtml(BaseTestCase):
    """Test case that we see the openapi."""

    url = base_url + "/openapi"

    def test_get(self):
        """Ensure that we can get the page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestOpenapiJson(BaseTestCase):
    """Test case that we can work with the openapi."""

    url = base_url + "/openapi.json"

    def test_get(self):
        """Ensure that we can get our openapi payload."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # And ensure we can parse it as json.
        _ = response.json

    def test_has_device_list_endpoint(self):
        """Ensure that we have the endpoint for the devices."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        paths = data.get("paths", {})
        self.assertTrue("/devices" in paths.keys())

    def test_has_userinfo_endpoint(self):
        """Ensure that we have the endpoint for the userinfo."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        paths = data.get("paths", {})
        self.assertTrue("/user-info" in paths.keys())
