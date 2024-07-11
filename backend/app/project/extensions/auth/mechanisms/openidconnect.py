# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""OpenIDConnect authentication mechanism."""

import operator

import requests
from cachetools import TTLCache, cachedmethod
from flask import current_app, request

from ....api.helpers.errors import AuthenticationFailedError
from .mixins import CreateNewUserByUserinfoMixin


class OpenIdConnectAuthMechanism(CreateNewUserByUserinfoMixin):
    """Mechanism to authenticate via OpenIDConnect."""

    def __init__(self, app=None):
        """Initialize the object."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Init the flask extension."""
        self.cache = TTLCache(
            maxsize=5000, ttl=app.config.get("OIDC_TOKEN_CACHING_SECONDS", 600)
        )

    def can_be_applied(self):
        """Check if we can use this mechanism here."""
        # We rely that the middleware to read the data from the
        # well known url run already on startup.
        if not current_app.config.get("OIDC_USERINFO_ENDPOINT"):
            return False
        # Then we need an Authorization header with a Bearer token.
        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            return False
        if not authorization_header.startswith("Bearer "):
            return False
        return True

    @cachedmethod(operator.attrgetter("cache"))
    def get_userinfo(self, authorization):
        """Return the userinfo from the IDP."""
        resp_userinfo = requests.get(
            current_app.config["OIDC_USERINFO_ENDPOINT"],
            headers={"Authorization": authorization},
        )
        if not resp_userinfo.ok:
            raise AuthenticationFailedError(
                "User could not be authenticated by openidconnect.",
                detail=resp_userinfo.text,
            )
            # It can be that there are changes on the IDP config.
            # However, those should not affect our get userinfo endpoint.
            # So if we can't authenticate here, we let another mechanism
            # do its try.
        return resp_userinfo.json()

    def authenticate(self):
        """Return a user object for our current request."""
        authorization = request.headers.get("Authorization")
        return self.authenticate_by_authorization(authorization)

    def authenticate_by_authorization(self, authorization):
        """Return a user object for our current request."""
        try:
            attributes = self.get_userinfo(authorization)
        except AuthenticationFailedError:
            # It can be that there are changes on the IDP config.
            # However, those should not affect our get userinfo endpoint.
            # So if we can't authenticate here, we let another mechanism
            # do its try.
            return None

        # Now we can be sure that we have some userinformation.
        identity = attributes.get(
            current_app.config.get("OIDC_USERDATA_IDENTITY_CLAIM", "sub"),
            # Fallback in case we try to use a different claim,
            # but only have the sub included.
            # Could be the case for github logins for example.
            attributes.get("sub"),
        )
        return self.get_user_or_create_new(identity, attributes)
