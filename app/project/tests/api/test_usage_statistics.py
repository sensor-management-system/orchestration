# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the usage statistics."""

from project import base_url
from project.api.models import Configuration, Contact, Device, Platform, Site, User
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestUsageStatistics(BaseTestCase):
    """Test class for the usage statistics."""

    url = base_url + "/usage-statistics"

    def test_get_empty(self):
        """Test with just the empty db."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 0,
                "platforms": 0,
                "configurations": 0,
                "users": 0,
                "sites": 0,
            },
        )

    def test_post_not_allowed(self):
        """Test that we can not post."""
        response = self.client.post(self.url, content_type="application/vnd.api+json")
        self.assertEqual(response.status_code, 405)

    def test_get_one_device(self):
        """Test the counts with one device."""
        device = Device(short_name="first device")
        db.session.add(device)
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 1,
                "platforms": 0,
                "configurations": 0,
                "users": 0,
                "sites": 0,
            },
        )

    def test_get_one_platform(self):
        """Test the count with one platform."""
        platform = Platform(short_name="first platform")
        db.session.add(platform)
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 0,
                "platforms": 1,
                "configurations": 0,
                "users": 0,
                "sites": 0,
            },
        )

    def test_get_one_configuration(self):
        """Test the count with one configuration."""
        configuration = Configuration(label="first configuration")
        db.session.add(configuration)
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 0,
                "platforms": 0,
                "configurations": 1,
                "users": 0,
                "sites": 0,
            },
        )

    def test_get_one_user(self):
        """Test the count with one user."""
        contact = Contact(given_name="N", family_name="B", email="nb@localhost")
        user = User(subject="nb", contact=contact)
        db.session.add_all([contact, user])
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 0,
                "platforms": 0,
                "configurations": 0,
                "users": 1,
                "sites": 0,
            },
        )

    def test_get_one_site(self):
        """Test the count with one site."""
        site = Site(label="Site", is_internal=True, is_public=False)
        db.session.add(site)
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 0,
                "platforms": 0,
                "configurations": 0,
                "users": 0,
                "sites": 1,
            },
        )

    def test_get_mixed(self):
        """Test the counts with some data for various models."""
        device1 = Device(short_name="first device")
        device2 = Device(short_name="second device")
        device3 = Device(short_name="third device")
        device4 = Device(short_name="fourth device")
        platform1 = Platform(short_name="first platform")
        platform2 = Platform(short_name="second platform")
        platform3 = Platform(short_name="third platform")
        configuration1 = Configuration(label="first configuration")
        configuration2 = Configuration(label="second configuration")
        contact = Contact(given_name="N", family_name="B", email="nb@localhost")
        user = User(subject="nb", contact=contact)
        site1 = Site(label="Site1", is_internal=True, is_public=False)
        site2 = Site(label="Site2", is_internal=False, is_public=True)
        db.session.add_all(
            [
                device1,
                device2,
                device3,
                device4,
                platform1,
                platform2,
                platform3,
                configuration1,
                configuration2,
                contact,
                user,
                site1,
                site2,
            ]
        )
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("counts", data.keys())
        self.assertEqual(
            data["counts"],
            {
                "devices": 4,
                "platforms": 3,
                "configurations": 2,
                "users": 1,
                "sites": 2,
            },
        )
