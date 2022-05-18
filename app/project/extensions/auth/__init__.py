"""Authentication middleware."""

from flask import g

from .mechanisms.openidconnect import OpenIdConnectAuthMechanism
from .mechanisms.session import SessionAuthMechanism


class Auth:
    """
    Authentication extension for our app here.

    This just tries to authenticate with various mechisms.
    The default one is OpenIdConnectAuthMechanism, but we can extend it
    at any time in the future (apikeys for example).
    We can also overwrite the mechisms for easier testing.
    """

    def __init__(self, app=None, mechanisms=None):
        """Init the object."""
        if mechanisms is None:
            mechanisms = [
                SessionAuthMechanism(app),
                OpenIdConnectAuthMechanism(app),
            ]
        self.mechanisms = mechanisms
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Init the flask extension."""
        # All the mechanisms are flask extensions themselves.
        for mechanism in self.mechanisms:
            mechanism.init_app(app)
        # Make sure we run this one for every request.
        # This is basically a middleware, to set the
        # user in the request object.
        app.before_request(self.try_authentification)
        # Register the teardown context.
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        """
        Teardown handler.

        Can be used to close connections etc.
        """
        pass

    def try_authentification(self):
        """Run the authentication mechanisms & try to set the user object."""
        g.user = None
        for mechanism in self.mechanisms:
            if mechanism.can_be_applied():
                user = mechanism.authenticate()
                if user and user.active:
                    g.user = user
                    break
