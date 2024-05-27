# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the tsm endpoint api."""

import json

from project import base_url
from project.api.models import Contact, TsmEndpoint, User
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestTsmEndpoints(BaseTestCase):
    """Test class for the tsm endpoints."""

    url = base_url + "/tsm-endpoints"

    def test_get_empty(self):
        """Ensure we can get an empty list if there is no data."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], [])

    def test_get_list(self):
        """Ensure we can get a list of tsm endpoints."""
        tsm_endpoint1 = TsmEndpoint(name="ABC", url="https://localhost")
        tsm_endpoint2 = TsmEndpoint(name="DEF", url="https://127.0.0.1")
        db.session.add_all([tsm_endpoint1, tsm_endpoint2])
        db.session.commit()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json["data"]), 2)
        self.assertEqual(resp.json["data"][0]["id"], str(tsm_endpoint1.id))
        self.assertEqual(resp.json["data"][0]["type"], "tsm_endpoint")
        self.assertEqual(resp.json["data"][0]["attributes"]["name"], "ABC")
        self.assertEqual(resp.json["data"][0]["attributes"]["url"], "https://localhost")

        self.assertEqual(resp.json["data"][1]["id"], str(tsm_endpoint2.id))
        self.assertEqual(resp.json["data"][1]["type"], "tsm_endpoint")
        self.assertEqual(resp.json["data"][1]["attributes"]["name"], "DEF")
        self.assertEqual(resp.json["data"][1]["attributes"]["url"], "https://127.0.0.1")

    def test_post_super_user(self):
        """Ensure we are not allowed to post data (not even as superuser)."""
        payload = {
            "data": {
                "type": "tsm_endpoint",
                "attributes": {
                    "name": "abc",
                    "url": "https://localhost",
                },
            }
        }
        contact = Contact(
            given_name="given",
            family_name="family",
            email="mail@localhost",
        )
        super_user = User(
            subject=contact.email,
            contact=contact,
            is_superuser=True,
        )
        db.session.add_all([contact, super_user])
        db.session.commit()

        with self.run_requests_as(super_user):
            resp = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 403)

    def test_get_non_existing(self):
        """Ensure we can get a 404 response if there is no data."""
        resp = self.client.get(f"{self.url}/1234567890")
        self.assertEqual(resp.status_code, 404)

    def test_get_one(self):
        """Ensure we can get one tsm endpoint."""
        tsm_endpoint1 = TsmEndpoint(name="ABC", url="https://localhost")
        db.session.add(tsm_endpoint1)
        db.session.commit()
        resp = self.client.get(f"{self.url}/{tsm_endpoint1.id}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"]["id"], str(tsm_endpoint1.id))
        self.assertEqual(resp.json["data"]["type"], "tsm_endpoint")
        self.assertEqual(resp.json["data"]["attributes"]["name"], "ABC")
        self.assertEqual(resp.json["data"]["attributes"]["url"], "https://localhost")

    def test_patch_super_user(self):
        """Ensure we can't patch - not even as super user."""
        tsm_endpoint1 = TsmEndpoint(name="ABC", url="https://localhost")
        contact = Contact(
            given_name="given",
            family_name="family",
            email="mail@localhost",
        )
        super_user = User(
            subject=contact.email,
            contact=contact,
            is_superuser=True,
        )
        db.session.add_all([tsm_endpoint1, contact, super_user])
        db.session.commit()
        payload = {
            "data": {
                "id": str(tsm_endpoint1.id),
                "type": "tsm_endpoint",
                "attributes": {
                    "name": "ABC D",
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{tsm_endpoint1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 403)

    def test_delete_super_user(self):
        """Ensure we can't delete - not even as super user."""
        tsm_endpoint1 = TsmEndpoint(name="ABC", url="https://localhost")
        contact = Contact(
            given_name="given",
            family_name="family",
            email="mail@localhost",
        )
        super_user = User(
            subject=contact.email,
            contact=contact,
            is_superuser=True,
        )
        db.session.add_all([tsm_endpoint1, contact, super_user])
        db.session.commit()
        with self.run_requests_as(super_user):
            resp = self.client.delete(f"{self.url}/{tsm_endpoint1.id}")
        self.assertEqual(resp.status_code, 403)
