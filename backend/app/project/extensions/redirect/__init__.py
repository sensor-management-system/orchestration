# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Redirect middleware."""
from flask import redirect, request


class RemoveSlashRedirectMiddlware:
    """
    Middleware to remove trailing slashes.

    This should help to explore the API within the browser.
    """

    supported_methods = ["GET", "HEAD", "OPTIONS"]

    def __init__(self, app=None):
        """Init the object."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Register the middleware for the app."""
        app.before_request(self.redirect_without_slash)

    def redirect_without_slash(self):
        """Check if we can & need to redirect."""
        if request.method in self.supported_methods:
            if request.path.endswith("/"):
                # Ensure we have a shorter path that we could use.
                without_slash = request.path[:-1]
                if without_slash:
                    target_url = without_slash
                    query_string = request.query_string.decode()
                    if query_string:
                        target_url += "?" + query_string
                    return redirect(target_url)
