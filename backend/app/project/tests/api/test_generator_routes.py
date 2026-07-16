# SPDX-FileCopyrightText: 2026
# - Nils Brinckmann <nils.brinckmann@gfz.de>
# - GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)
#
# SPDX-License-Identifier: EUPL-1.2
"""Tests for the generator routes."""

from unittest.mock import patch

from project import base_url
from project.api.models import Contact, Device, Organization, Platform, User
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestGenerateSerialNumber(BaseTestCase):
    """Test cases for the generation of serial numbers."""

    url = base_url + "/controller/generators/serial-number"

    def test_without_user(self):
        """Ensure we can run it without a user."""
        with patch(
            "project.views.generator_routes.generate_char_part"
        ) as mock_char_part:
            mock_char_part.return_value = "AAAA"
            with patch(
                "project.views.generator_routes.generate_number_part"
            ) as mock_number_part:
                mock_number_part.return_value = "1234"
                resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], "SMS-AAAA-1234")

    def test_with_user_without_organization(self):
        """Ensure that there is still the fallback organization part if we have a user without an organization."""
        contact = Contact(
            given_name="test", family_name="user", email="test.user@localhost"
        )
        user = User(contact=contact, subject=contact.email)

        db.session.add_all([contact, user])
        db.session.commit()

        with patch(
            "project.views.generator_routes.generate_char_part"
        ) as mock_char_part:
            mock_char_part.return_value = "AAAA"
            with patch(
                "project.views.generator_routes.generate_number_part"
            ) as mock_number_part:
                mock_number_part.return_value = "1234"
                with self.run_requests_as(user):
                    resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], "SMS-AAAA-1234")

    def test_with_user_with_organization_without_abbreviation(self):
        """Ensure there is the fallback organization part if we have a user without organization abbreviation."""
        organization = Organization(name="local")
        contact = Contact(
            given_name="test",
            family_name="user",
            email="test.user@localhost",
            organization=organization.name,
        )
        user = User(contact=contact, subject=contact.email)

        db.session.add_all([contact, organization, user])
        db.session.commit()

        with patch(
            "project.views.generator_routes.generate_char_part"
        ) as mock_char_part:
            mock_char_part.return_value = "AAAA"
            with patch(
                "project.views.generator_routes.generate_number_part"
            ) as mock_number_part:
                mock_number_part.return_value = "1234"
                with self.run_requests_as(user):
                    resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], "SMS-AAAA-1234")

    def test_with_user_with_organization_and_abbreviation(self):
        """Ensure the organization abbreviation is used."""
        organization = Organization(name="local", abbreviation="LOC")
        contact = Contact(
            given_name="test",
            family_name="user",
            email="test.user@localhost",
            organization=organization.name,
        )
        user = User(contact=contact, subject=contact.email)

        db.session.add_all([contact, organization, user])
        db.session.commit()

        with patch(
            "project.views.generator_routes.generate_char_part"
        ) as mock_char_part:
            mock_char_part.return_value = "AAAA"
            with patch(
                "project.views.generator_routes.generate_number_part"
            ) as mock_number_part:
                mock_number_part.return_value = "1234"
                with self.run_requests_as(user):
                    resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], "LOC-AAAA-1234")

    def test_with_explicit_abbreviation(self):
        """Ensure we can set the organization part explicitly."""
        with patch(
            "project.views.generator_routes.generate_char_part"
        ) as mock_char_part:
            mock_char_part.return_value = "AAAA"
            with patch(
                "project.views.generator_routes.generate_number_part"
            ) as mock_number_part:
                mock_number_part.return_value = "1234"
                resp = self.client.get(f"{self.url}?organization_part=HELMHOLTZ")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], "HELM-AAAA-1234")

    def test_with_seed_and_existing_serial_number(self):
        """Ensure we generate new serial numbers if there are entries that already use them."""
        resp1 = self.client.get(f"{self.url}?seed=42")
        self.assertEqual(resp1.status_code, 200)
        sn1 = resp1.json["data"]

        resp2 = self.client.get(f"{self.url}?seed=42")
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp2.json["data"], sn1)

        existing_device = Device(
            short_name="test_device",
            serial_number=sn1,
        )
        db.session.add(existing_device)
        db.session.commit()

        resp3 = self.client.get(f"{self.url}?seed=42")
        self.assertEqual(resp3.status_code, 200)
        sn3 = resp3.json["data"]

        self.assertNotEqual(sn1, sn3)

        existing_platform = Platform(
            short_name="test platform",
            serial_number=sn3,
        )
        db.session.add(existing_platform)
        db.session.commit()

        resp4 = self.client.get(f"{self.url}?seed=42")
        self.assertEqual(resp4.status_code, 200)
        sn4 = resp4.json["data"]

        self.assertNotEqual(sn1, sn4)
        self.assertNotEqual(sn3, sn4)
