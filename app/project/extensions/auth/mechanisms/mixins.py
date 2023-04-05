# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Mixin classes that may be used for multiple authentification mechanisms."""

from ....api.models import Contact, User
from ....api.models.base_model import db


class CreateNewUserByUserinfoMixin:
    """
    Mixin to create new users if we need to do so.

    As we rely on the data that we get from the idp, we
    create new users in case there is the very first request.
    If we find existing ones, we can go on with those.
    """

    @staticmethod
    def get_user_or_create_new(identity, attributes):
        """Return an existing user or create a new one."""
        # We check if we find a user for this identity entry.
        found_user = db.session.query(User).filter_by(subject=identity).one_or_none()
        if found_user:
            return found_user

        # We haven't found any user with the subject.
        # But as we rely on the IDP, we will insert it in the database.
        # However, every user gets a contact.
        # Do we have one already?
        email = attributes["email"]
        contact = db.session.query(Contact).filter_by(email=email).one_or_none()
        if contact:
            if not contact.active:
                contact.given_name = attributes["given_name"]
                contact.family_name = attributes["family_name"]
                contact.active = True
                db.session.add(contact)
        if not contact:
            contact = Contact(
                given_name=attributes["given_name"],
                family_name=attributes["family_name"],
                email=attributes["email"],
                active=True,
            )
            db.session.add(contact)
        apikey = User.generate_new_apikey()
        user = User(subject=identity, contact=contact, active=True, apikey=apikey)
        db.session.add(user)
        db.session.commit()
        return user
