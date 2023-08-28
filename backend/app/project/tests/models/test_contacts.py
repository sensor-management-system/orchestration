# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0


"""Test cases for the contacts model."""

from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.tests.base import BaseTestCase, generate_userinfo_data


class TestContactModels(BaseTestCase):
    """Tests for the contact model."""

    def test_add_contact_model(self):
        """Ensure we can add a contact model to the database."""
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        db.session.add(contact)
        db.session.commit()

        contact = db.session.query(Contact).filter_by(id=contact.id).one()
        self.assertIn(contact.email, contact.email)

    def test_text_search_fields(self):
        """Ensure the most important fields are in the fields for full text search."""
        text_fields = Contact.text_search_fields()
        self.assertTrue("given_name" in text_fields)
        self.assertTrue("family_name" in text_fields)
        self.assertFalse("created_by_id" in text_fields)
