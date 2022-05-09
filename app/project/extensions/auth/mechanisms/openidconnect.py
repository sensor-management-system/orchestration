"""OpenIDConnect authentification mechanism."""

import requests
from cachetools import TTLCache, cached
from flask import request, current_app
from .mixins import CreateNewUserByUserinfoMixin


class OpenIdConnectAuthMechanism(CreateNewUserByUserinfoMixin):
    """Mechanism to authenticate via OpenIDConnect."""

    def __init__(self, app=None):
        """Initialyze the object."""
        self.config = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Init the flask extension."""
        self.config = self.load_config(app)
        app.teardown_appcontext(self.teardown)

    def load_config(self, app):
        if not app.config.get("OIDC_WELL_KNOWN_URL"):
            app.logger.warn(
                "No OIDC_WELL_KNOWN_URL given. We can't use OpenIdConnectAuthMechanism."
            )
            return None
        resp = requests.get(app.config["OIDC_WELL_KNOWN_URL"])
        # If the OIDC_WELL_KNOWN_URL is given, we expect that we get
        # a proper answer so that we can work with it.
        resp.raise_for_status()
        return resp.json()

    def teardown(self, exception):
        """
        Cleanup on app teardown.

        Can be used to close connections etc. Currently unused.
        """
        pass

    def can_be_applied(self):
        """Check if we can use this mechanism here."""
        # If we don't have a config, there is no way to use this here.
        if not self.config:
            return False
        # Then we need an Authorization header with a Bearer token.
        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            return False
        if not authorization_header.startswith("Bearer "):
            return False
        return True



    @cached(cache=TTLCache(maxsize=5000, ttl=600))
    def authenticate(self):
        """Return a user object for our current request."""
        resp_userinfo = requests.get(
            self.config["userinfo_endpoint"],
            headers={"Authorization": request.headers.get("Authorization")},
        )
        if not resp_userinfo.ok:
            # It can be that there are changes on the IDP config.
            # However those should not effect our get userinfo endpoint.
            # So if we can't authenticate here, we let another mechanism
            # do its try.
            return None

        # Now we can be sure that we have some userinformation.
        attributes = resp_userinfo.json()
        identity = attributes.get(
            current_app.config.get("OIDC_USERDATA_IDENTITY_CLAIM", "sub")
        )
        return self.get_user_or_create_new(identity, attributes)
