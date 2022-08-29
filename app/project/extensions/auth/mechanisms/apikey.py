"""Mechanism to authenticate a user by apikey."""

from flask import request

from ....api.models import User
from ....api.models.base_model import db


class ApikeyAuthMechanism:
    """Implementation to check the X-APIKEY header."""

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
        """Return true if we have an X-APIKEY header."""
        apikey_header = request.headers.get("X-APIKEY")
        if not apikey_header:
            return False
        return True

    def authenticate(self):
        """Return the user for the apikey."""
        apikey_header = request.headers.get("X-APIKEY")
        if apikey_header:
            return (
                db.session.query(User)
                .filter(User.apikey == apikey_header)
                .one_or_none()
            )
        return None
