# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Mechanism to authenticate a user by apikey."""

from flask import request

from ....api.models import User
from ....api.models.base_model import db


class ApikeyAuthMechanism:
    """Implementation to check the X-APIKEY header or the apikey query parameter."""

    def __init__(self, app=None):
        """Init the object."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Init the app.

        This method is needed to fullfil the interface for flask extensions.
        """
        pass

    @staticmethod
    def can_be_applied():
        """Return true if we have an X-APIKEY header or the query parameter."""
        apikey_header = request.headers.get("X-APIKEY")
        if apikey_header:
            return True

        apikey_query_parameter = request.values.get("apikey")
        if apikey_query_parameter:
            return True

        return False

    def authenticate(self):
        """Return the user for the apikey."""
        apikey_header = request.headers.get("X-APIKEY")
        if apikey_header:

            return self.find_user_by_apikey(apikey_header)
        apikey_query_parameter = request.values.get("apikey")
        if apikey_query_parameter:
            return self.find_user_by_apikey(apikey_query_parameter)

        return None

    def find_user_by_apikey(self, apikey):
        """Return a user or none for the given apikey."""
        return db.session.query(User).filter(User.apikey == apikey).one_or_none()
