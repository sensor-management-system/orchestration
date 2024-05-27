# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

from project.api.models import Contact
from project.api.models.base_model import db
from project.api.models.user import User
from project.tests.base import BaseTestCase, generate_userinfo_data

from project.tests.base import fake


def add_user():
    userinfo = generate_userinfo_data()
    c = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    user = User(subject=fake.pystr(), contact=c)

    db.session.add_all([c, user])
    db.session.commit()

    return user


class TestUsersModel(BaseTestCase):
    """
    Test User Services
    """

    def test_add_user_model(self):
        """""Ensure Add user model """
        user = add_user()

        u = db.session.query(User).filter_by(id=user.id).one()
        self.assertIn(u.subject, user.subject)
