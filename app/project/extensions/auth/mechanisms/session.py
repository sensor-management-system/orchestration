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

    def can_be_applied(self):
        """Return true if we have an user id in the session."""
        # Sessions are stored encrypted, so only work with validated
        # data here that can't be currupted by a user (as long as they
        # don't know the flask secret).
        return "user_id" in session

    def authenticate(self):
        """Try to find the user for the given user id."""
        user_id = session["user_id"]
        return db.session.query(User).filter_by(id=user_id).one_or_none()
