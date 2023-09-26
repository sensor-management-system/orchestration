# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resources to modify the current user."""

import datetime

import pytz
from flask import g
from flask_rest_jsonapi import ResourceList

from ..helpers.errors import MethodNotAllowed, UnauthorizedError
from ..models import User
from ..models.base_model import db


class RevokeApikey(ResourceList):
    """Resource to allow the user to revoke the apikey - and to get a new one."""

    def get(self):
        """Get is not allowed."""
        raise MethodNotAllowed("Endpoint can only be used with POST method.")

    def post(self):
        """Take the user of the request set a new apikey & return it."""
        if not g.user:
            raise UnauthorizedError("Authentication required")
        g.user.apikey = User.generate_new_apikey()
        db.session.add(g.user)
        db.session.commit()

        response = {
            "data": {
                "type": "user",
                "id": str(g.user.id),
                "attributes": {"apikey": g.user.apikey},
            }
        }
        return response


class AcceptTermsOfUse(ResourceList):
    """Resource to allow the user to agree to terms of use + set the field in db."""

    def get(self):
        """Get is not allowed."""
        raise MethodNotAllowed("Endpoint can only be used with POST method.")

    def post(self):
        """Take the user of the request and set the terms of use agreement date & return it."""
        if not g.user:
            raise UnauthorizedError("Authentication required")
        now = self.get_current_time()
        g.user.terms_of_use_agreement_date = now
        db.session.add(g.user)
        db.session.commit()

        response = {
            "data": {
                "type": "user",
                "id": str(g.user.id),
                "attributes": {
                    "terms_of_use_agreement_date": g.user.terms_of_use_agreement_date
                },
            }
        }
        return response

    def get_current_time(self):
        """Get the current datetime (helper method for easier mocking)."""
        return datetime.datetime.now(tz=pytz.utc)
