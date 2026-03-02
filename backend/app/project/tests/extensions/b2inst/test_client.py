# SPDX-FileCopyrightText: 2026
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Test the B2InstClient."""

import io
import json
from unittest import TestCase
from unittest.mock import patch

from project.extensions.b2inst.client import B2InstClient


class TestB2InstClient(TestCase):
    """Test the B2instClient methods."""

    @patch("urllib.request.urlopen")
    def test_create_draft_record(self, urlopen):
        """Test the method to create a new draft record."""
        # The result here is incomplete; just something for the mock.
        urlopen.return_value = io.StringIO(json.dumps({"id": "abcd"}))
        client = B2InstClient("https://localhost:8000", "abcd")
        # The metadata here is incomplete; just something for the mock.
        data = {"metadata": {"Name": "something"}}
        result = client.create_draft_record(data)

        urlopen.assert_called_once()
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url, "https://localhost:8000/api/records?access_token=abcd"
        )
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.data, b'{"metadata": {"Name": "something"}}')
        self.assertEqual(request.headers, {"Content-type": "application/json"})
        self.assertEqual(result, {"id": "abcd"})

    @patch("urllib.request.urlopen")
    def test_publish_record(self, urlopen):
        """Test the method to publish a record."""
        urlopen.return_value = io.StringIO(json.dumps({}))
        client = B2InstClient("https://localhost:8000", "abcd")
        result = client.publish_record("42")

        urlopen.assert_called_once()
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "https://localhost:8000/api/records/42/draft/actions/publish?access_token=abcd",
        )
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.data, None)
        self.assertEqual(result, {})

    @patch("urllib.request.urlopen")
    def test_create_new_draft(self, urlopen):
        """Test the method to create a new draft from an existing record."""
        urlopen.return_value = io.StringIO(json.dumps({}))
        client = B2InstClient("https://localhost:8000", "abcd")
        result = client.create_new_draft("42")

        urlopen.assert_called_once()
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "https://localhost:8000/api/records/42/draft?access_token=abcd",
        )
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.data, None)
        self.assertEqual(result, {})

    @patch("urllib.request.urlopen")
    def test_create_new_version(self, urlopen):
        """Test the method to create a new version."""
        urlopen.return_value = io.StringIO(json.dumps({}))
        client = B2InstClient("https://localhost:8000", "abcd")
        result = client.create_new_version("42")

        urlopen.assert_called_once()
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "https://localhost:8000/api/records/42/versions?access_token=abcd",
        )
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.data, None)
        self.assertEqual(result, {})

    @patch("urllib.request.urlopen")
    def test_update_draft(self, urlopen):
        """Test the method to update the draft data."""
        urlopen.return_value = io.StringIO(json.dumps({}))
        client = B2InstClient("https://localhost:8000", "abcd")
        # The metadata here is incomplete; just something for the mock.
        data = {"metadata": {"Name": "something"}}
        result = client.update_draft("42", data)

        urlopen.assert_called_once()
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "https://localhost:8000/api/records/42/draft?access_token=abcd",
        )
        self.assertEqual(request.method, "PUT")
        self.assertEqual(request.data, b'{"metadata": {"Name": "something"}}')
        self.assertEqual(request.headers, {"Content-type": "application/json"})
        self.assertEqual(result, {})

    @patch("urllib.request.urlopen")
    def test_add_communities(self, urlopen):
        """Test the method to add records to a community."""
        urlopen.return_value = io.StringIO(json.dumps({}))
        client = B2InstClient("https://localhost:8000", "abcd")
        result = client.add_communities("42", ["abc"])

        urlopen.assert_called_once()
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "https://localhost:8000/api/records/42/communities?access_token=abcd",
        )
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.data, b'{"communities": [{"id": "abc"}]}')
        self.assertEqual(request.headers, {"Content-type": "application/json"})
        self.assertEqual(result, {})

    @patch("urllib.request.urlopen")
    def test_get_communities(self, urlopen):
        """Test the get communities method."""
        urlopen.return_value = io.StringIO(
            json.dumps(
                {"hits": {"hits": [{"id": "c1", "metadata": {"title": "Community 1"}}]}}
            )
        )
        client = B2InstClient("https://localhost:8000", "abcd")
        result = client.get_communities()
        urlopen.assert_called_once()
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://localhost:8000/api/communities")
        self.assertEqual(
            result,
            {
                "hits": {
                    "hits": [
                        {
                            "id": "c1",
                            "metadata": {
                                "title": "Community 1",
                            },
                        }
                    ]
                }
            },
        )

    def test_get_record_frontend_url(self):
        """Test the method to get the url that is rendered in the ui of the b2inst."""
        client = B2InstClient("https://localhost:8000", "abcd")
        result = client.get_record_frontend_url("42")
        expected = "https://localhost:8000/records/42"
        self.assertEqual(result, expected)

    @patch("urllib.request.urlopen")
    def test_ping(self, urlopen):
        """Test the ping method."""
        urlopen.return_value = io.BytesIO(b"OK")
        client = B2InstClient("https://localhost:8000", "abcd")
        result = client.ping()
        urlopen.assert_called_once()
        request = urlopen.call_args.args[0]
        # We use the same url as for the communities
        self.assertEqual(request.full_url, "https://localhost:8000/api/ping")
        self.assertEqual(result, b"OK")
