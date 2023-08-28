# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Auth mechanism using the flask session object."""

from flask import session

from ....api.models import User
from ....api.models.base_model import db


class SessionAuthMechanism:
    """Auth mechanism implementation using the flask session object."""

    def __init__(self, app=None):
        """Init the object."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Init the extension with the app.

        This is part of the interface for flask extensions.
        """
        pass

    @staticmethod
    def can_be_applied():
        """Return true if we have an user id in the session."""
        # Sessions are stored encrypted, so only work with validated
        # data here that can't be currupted by a user (as long as they
        # don't know the flask secret).
        return "user_id" in session

    @staticmethod
    def authenticate():
        """Try to find the user for the given user id."""
        user_id = session["user_id"]
        return db.session.query(User).filter_by(id=user_id).one_or_none()
