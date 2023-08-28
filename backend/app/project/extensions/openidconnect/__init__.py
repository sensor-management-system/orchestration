# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Classes to interact with openidconnect."""

import requests


class WellKnownUrlConfigLoader:
    """Extension to store the data from well known url into the app config."""

    def __init__(self, app=None):
        """Initialize the instance."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize with the app.

        Loads data from the well known url & stores them in the app config.
        """
        if not app.config["TESTING"]:
            well_known_url = app.config["OIDC_WELL_KNOWN_URL"]
            resp = requests.get(well_known_url)
            resp.raise_for_status()
            config = resp.json()
            # And we set the config in our application config.
            # This way all the others can rely on them to be provided
            # within their request context.
            app.config["OIDC_USERINFO_ENDPOINT"] = config["userinfo_endpoint"]
            app.config["OIDC_AUTHORIZATION_ENDPOINT"] = config["authorization_endpoint"]
            app.config["OIDC_TOKEN_ENDPOINT"] = config["token_endpoint"]
