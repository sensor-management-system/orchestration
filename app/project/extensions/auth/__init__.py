"""Authentication middleware."""

from flask import g


class Auth:
    """
    Authentication extension for our app here.

    This just tries to authenticate with various mechanisms.
    The default one is OpenIdConnectAuthMechanism, but we can extend it
    at any time in the future (apikeys for example).
    We can also overwrite the mechanisms for easier testing.
    """

    def __init__(self, app=None, mechanisms=None):
        """Init the object."""
        if mechanisms is None:
            mechanisms = []
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

    def try_authentification(self):
        """Run the authentication mechanisms & try to set the user object."""
        g.user = None
        for mechanism in self.mechanisms:
            if mechanism.can_be_applied():
                user = mechanism.authenticate()
                if user and user.active:
                    g.user = user
                    break
