# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: EUPL-1.2

"""Regression tests for the removed arbitrary-URL proxy."""

import unittest
from unittest.mock import patch

from project import base_url, create_app


class TestRemovedProxy(unittest.TestCase):
    """The old endpoint must not make outbound requests."""

    def test_proxy_is_not_registered(self):
        """Requests to the removed proxy return 404 without fetching a URL."""
        app = create_app()
        prefix = base_url
        with app.test_client() as client, patch("requests.get") as get:
            response = client.get(
                f"{prefix}/proxy", query_string={"url": "http://127.0.0.1/"}
            )
        self.assertEqual(response.status_code, 404)
        get.assert_not_called()
