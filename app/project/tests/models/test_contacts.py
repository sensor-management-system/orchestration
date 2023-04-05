# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.tests.base import BaseTestCase, generate_userinfo_data


class TestContactModels(BaseTestCase):
    """
    Test Contact Model
    """

    def test_add_contact_model(self):
        """""Ensure Add contact model """
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
