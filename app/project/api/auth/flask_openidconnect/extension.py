"""Extension class for openidconnect."""

import requests
from cachetools import TTLCache, cached
from flask import _request_ctx_stack, current_app, request

from ...helpers.errors import UnauthorizedError


class OpenIDConnect:
    """
    Authentication extension to use flask with open id connect pkce flow.

    This is a flask extension to handle the details of the open id connect
    pkce flow & to hide the details of internal implementation (which
    uses JWT & flask_jwt_extended).
    """

    def __init__(self, app=None):
        """Init the object of the extension."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Init the app with this extension."""
        app.config.setdefault(
            "OIDC_WELL_KNOWN_URL",
            "https://login-dev.helmholtz.de/oauth2/.well-known/openid-configuration",
        )
        app.config.setdefault(
            "OIDC_USERDATA_IDENTITY_CLAIM",
            "sub",
        )
        # Register the teardown context.
        app.teardown_appcontext(self.teardown)
        self._set_error_handler_callbacks(app)

    def _set_error_handler_callbacks(self, app):
        """Add the error handlers for the app."""
        # We need to register & handle the exceptions
        # that we throw (even that those are ErrorResponse instances
        # that are mostly handled in the flask json api extension).
        @app.errorhandler(UnauthorizedError)
        def handle_unauthorized_error(e):
            """Handle the UnauthorizedError."""
            return e.respond()

    def teardown(self, exception):
        """
        Teardown handler.

        Can be used to close connections etc.
        """
        pass

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def _get_oidc_config(self):
        """
        Query the config from the server.

        As this data is intended to be consist over a longer time, we
        also cache the result here.
        """
        resp = requests.get(current_app.config["OIDC_WELL_KNOWN_URL"])
        resp.raise_for_status()
        return resp.json()

    def _get_userinfo(self):
        """Get the userinfo from the server by sending the access token."""
        config = self._get_oidc_config()
        userinfo_endpoint = config["userinfo_endpoint"]

        authorization_header = request.headers.get("Authorization")
        resp_userinfo = requests.get(
            userinfo_endpoint,
            headers={"Authorization": authorization_header},
        )
        resp_userinfo.raise_for_status()
        return resp_userinfo.json()

    def _verify_valid_access_token_in_request(self):
        """Verify that we have the valid access token."""
        try:
            attributes = self._get_userinfo()
            identity = attributes.get(
                current_app.config["OIDC_USERDATA_IDENTITY_CLAIM"]
            )
            return identity, attributes
        except requests.exceptions.RequestException:
            # In case we have a problem with our requests
            # (config / userinfo), we want to deny the access.
            raise UnauthorizedError("No valid access token.")

    def verify_valid_access_token_in_request_and_set_user(self):
        """
        Verify that we have the valid access token.

        Makes sure that we also load our user from the user_lookup_loader.
        """
        identity, attributes = self._verify_valid_access_token_in_request()
        user_lookup = self._oidc_user_lookup_loader
        user = user_lookup(identity, attributes)
        _request_ctx_stack.top.oidc_user = user

    def user_lookup_loader(self, callback):
        """
        Register a callback to extract the user from the database.

        The callback will be used with 2 arguments:
        - one string with the identitifer
        - the overall dict with the user info.
        The method should return a user object (specific for the app).
        """
        self._oidc_user_lookup_loader = callback

    def get_current_user(self):
        """
        Return the current user.

        It returns the user that was identified with
        the access token & the app specific user lookup loader.
        """
        if hasattr(_request_ctx_stack.top, "oidc_user"):
            return _request_ctx_stack.top.oidc_user
        return None
