"""OpenIDConnect authentification mechanism."""

import operator

import requests
from cachetools import TTLCache, cachedmethod
from flask import current_app, request

from .mixins import CreateNewUserByUserinfoMixin


class OpenIdConnectAuthMechanism(CreateNewUserByUserinfoMixin):
    """Mechanism to authenticate via OpenIDConnect."""

    def __init__(self, app=None):
        """Initialyze the object."""
        self.config = None
        self.config_loaded = False
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Init the flask extension."""
        app.teardown_appcontext(self.teardown)
        self.cache = TTLCache(
            maxsize=5000, ttl=app.config.get("OIDC_SECONDS_CACHING", 600)
        )

    def load_config(self, app):
        """Load the config for the IDP from the well known url."""
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
        if not self.config_loaded:
            self.config = self.load_config(current_app)
            self.config_loaded = True

        if not self.config:
            return False
        # Then we need an Authorization header with a Bearer token.
        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            return False
        if not authorization_header.startswith("Bearer "):
            return False
        return True

    @cachedmethod(operator.attrgetter("cache"))
    def get_userinfo(self):
        """Return the userinfo from the IDP."""
        resp_userinfo = requests.get(
            self.config["userinfo_endpoint"],
            headers={"Authorization": request.headers.get("Authorization")},
        )
        if not resp_userinfo.ok:
            raise GetUserinfoException()
            # It can be that there are changes on the IDP config.
            # However those should not effect our get userinfo endpoint.
            # So if we can't authenticate here, we let another mechanism
            # do its try.
        return resp_userinfo.json()

    def authenticate(self):
        """Return a user object for our current request."""
        try:
            attributes = self.get_userinfo()
        except GetUserinfoException:
            # It can be that there are changes on the IDP config.
            # However those should not effect our get userinfo endpoint.
            # So if we can't authenticate here, we let another mechanism
            # do its try.
            return None

        # Now we can be sure that we have some userinformation.
        identity = attributes.get(
            current_app.config.get("OIDC_USERDATA_IDENTITY_CLAIM", "sub")
        )
        return self.get_user_or_create_new(identity, attributes)


class GetUserinfoException(Exception):
    """
    Exception that indicates that we can't query for userinformation.

    This can be due to several reasons, but in any case it indicates
    that we can't make sure that the token we got is valid.
    """

    pass
