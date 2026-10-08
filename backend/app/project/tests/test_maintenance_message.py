# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the fixed-purpose maintenance endpoint (no database required)."""

import unittest
from unittest.mock import MagicMock, patch

import requests
from flask import Flask

from project.views.maintenance import MAX_DOCUMENT_BYTES, maintenance_routes


class TestMaintenanceMessage(unittest.TestCase):
    """Only trusted server configuration can select the document."""

    def setUp(self):
        """Register only the maintenance blueprint."""
        self.app = Flask(__name__)
        self.app.config.update(
            MAINTENANCE_DOCUMENT_URL=(
                "https://codebase.helmholtz.cloud/message.md"
            ),
        )
        self.app.register_blueprint(maintenance_routes)
        self.client = self.app.test_client()
        self.url = maintenance_routes.url_prefix + "/maintenance-message"

    def mock_response(self, get, status=200, content=b"# Maintenance"):
        """Provide a streamed response without making a network request."""
        response = MagicMock()
        response.status_code = status
        response.iter_content.return_value = [content]
        get.return_value.__enter__.return_value = response

    @patch("project.views.maintenance.requests.get")
    def test_fixed_url_without_cache(self, get):
        """Ignore client URLs and fetch fresh documents on every request."""
        self.mock_response(get)
        response = self.client.get(
            self.url, query_string={"url": "http://localhost/"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"# Maintenance")
        self.assertEqual(response.content_type, "text/plain; charset=utf-8")
        get.assert_called_once_with(
            self.app.config["MAINTENANCE_DOCUMENT_URL"],
            timeout=(3, 5),
            allow_redirects=False,
            stream=True,
            headers={"Accept": "text/plain"},
        )
        self.mock_response(get, content=b"Updated maintenance message")
        response = self.client.get(self.url)
        self.assertEqual(response.data, b"Updated maintenance message")
        self.assertEqual(get.call_count, 2)

    @patch("project.views.maintenance.requests.get")
    def test_configured_host_without_allowlist(self, get):
        """The server-configured URL needs no separate hostname setting."""
        self.app.config["MAINTENANCE_DOCUMENT_URL"] = (
            "https://maintenance.example.org/message.md"
        )
        self.mock_response(get)
        self.assertEqual(self.client.get(self.url).status_code, 200)
        self.assertEqual(
            get.call_args.args[0], self.app.config["MAINTENANCE_DOCUMENT_URL"]
        )

    @patch("project.views.maintenance.requests.get")
    def test_disabled(self, get):
        """No configuration means no message and no network request."""
        self.app.config["MAINTENANCE_DOCUMENT_URL"] = ""
        self.assertEqual(self.client.get(self.url).status_code, 204)
        get.assert_not_called()


    @patch("project.views.maintenance.requests.get")
    def test_upstream_errors(self, get):
        """Never follow redirects or return upstream error bodies."""
        for status in [301, 302, 404, 500]:
            with self.subTest(status=status):
                self.mock_response(get, status=status)
                response = self.client.get(self.url)
                self.assertEqual(response.status_code, 502)
                self.assertEqual(response.data, b"")

    @patch("project.views.maintenance.requests.get")
    def test_oversized_document(self, get):
        """Bound downloaded document size."""
        self.mock_response(get, content=b"a" * (MAX_DOCUMENT_BYTES + 1))
        self.assertEqual(self.client.get(self.url).status_code, 502)

    @patch("project.views.maintenance.requests.get")
    def test_timeout_is_not_cached(self, get):
        """Retry the upstream request after a failure."""
        get.side_effect = requests.Timeout()
        self.assertEqual(self.client.get(self.url).status_code, 502)
        self.assertEqual(self.client.get(self.url).status_code, 502)
        self.assertEqual(get.call_count, 2)
