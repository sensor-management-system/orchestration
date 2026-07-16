# SPDX-FileCopyrightText: 2026
# - Nils Brinckmann <nils.brinckmann@gfz.de>
# - GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Here are tests for the auth middleware."""

from project.api.models import Contact, Organization, User
from project.api.models.base_model import db
from project.extensions.auth.mechanisms.mixins import CreateNewUserByUserinfoMixin
from project.tests.base import BaseTestCase


class TestGetUserOrCreateNew(BaseTestCase):
    """Some tests for the mixin to find or create users based on the userinfo attributes of the IDP."""

    def test_it_should_return_an_existing_user_by_identity_field(self):
        """Test that we find an existing contact."""
        contact = Contact(
            given_name="test",
            family_name="user",
            email="testuser@localhost",
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all([contact, user])
        db.session.commit()

        identity = "testuser@localhost"
        attributes = {}

        self.assertEqual(db.session.query(Contact).count(), 1)
        self.assertEqual(db.session.query(User).count(), 1)
        found_user = CreateNewUserByUserinfoMixin.get_user_or_create_new(
            identity, attributes
        )
        self.assertEqual(found_user, user)
        self.assertEqual(db.session.query(Contact).count(), 1)
        self.assertEqual(db.session.query(User).count(), 1)

    def test_it_should_add_a_new_contact_and_user(self):
        """Test that we can create a new contact if we didn't find an existing."""
        identity = "testuser@localhost"
        attributes = {
            "given_name": "test",
            "family_name": "user",
            "email": "long.testuser@localhost",
        }

        self.assertEqual(db.session.query(Contact).count(), 0)
        self.assertEqual(db.session.query(User).count(), 0)
        new_user = CreateNewUserByUserinfoMixin.get_user_or_create_new(
            identity, attributes
        )
        self.assertEqual(db.session.query(Contact).count(), 1)
        self.assertEqual(db.session.query(User).count(), 1)
        self.assertEqual(db.session.query(Organization).count(), 0)

        self.assertEqual(new_user.subject, "testuser@localhost")
        contact = new_user.contact
        self.assertEqual(contact.given_name, "test")
        self.assertEqual(contact.family_name, "user")
        self.assertEqual(contact.email, "long.testuser@localhost")

    def test_it_should_associate_it_with_a_known_organization(self):
        """Ensure that we also extract the organization by the domain."""
        identity = "tuser@gfz.de"
        attributes = {
            "given_name": "test",
            "family_name": "user",
            "email": "test.user@gfz.de",
        }

        self.assertEqual(db.session.query(Contact).count(), 0)
        self.assertEqual(db.session.query(User).count(), 0)
        new_user = CreateNewUserByUserinfoMixin.get_user_or_create_new(
            identity, attributes
        )
        self.assertEqual(db.session.query(Contact).count(), 1)
        self.assertEqual(db.session.query(User).count(), 1)
        self.assertEqual(db.session.query(Organization).count(), 1)

        self.assertEqual(new_user.subject, "tuser@gfz.de")
        contact = new_user.contact
        self.assertEqual(contact.given_name, "test")
        self.assertEqual(contact.family_name, "user")
        self.assertEqual(contact.email, "test.user@gfz.de")
        self.assertEqual(contact.organization, "GFZ Helmholtz Centre for Geosciences")
        organization = db.session.query(Organization).first()
        self.assertEqual(organization.name, contact.organization)

    def test_it_should_not_create_a_new_organization_if_that_already_exists(self):
        """Ensure that we reuse existing organizations."""
        organization = Organization(
            name="GFZ Helmholtz Centre for Geosciences",
        )
        db.session.add(organization)
        db.session.commit()

        identity = "tuser@gfz.de"
        attributes = {
            "given_name": "test",
            "family_name": "user",
            "email": "test.user@gfz.de",
        }

        self.assertEqual(db.session.query(Contact).count(), 0)
        self.assertEqual(db.session.query(User).count(), 0)
        CreateNewUserByUserinfoMixin.get_user_or_create_new(identity, attributes)
        self.assertEqual(db.session.query(Contact).count(), 1)
        self.assertEqual(db.session.query(User).count(), 1)
        self.assertEqual(db.session.query(Organization).count(), 1)
