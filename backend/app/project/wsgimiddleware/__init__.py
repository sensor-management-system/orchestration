# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""
WSGI middleware.

Reason for this is that neighter flask nor werkzeug lets us change some of the
elements in the request (like the headers).
"""

from urllib.parse import parse_qs


class AcceptHeaderMiddleware:
    """Middleware to overwrite the accept header."""

    def __init__(self, wsgi_app):
        """Init with the wsgi app."""
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        """
        Run the middleware and change the accept header if wanted.

        The idea is that we want to allow to set accept header
        using the querystring parameter.

        That way it is easier to open some routes with specific
        accept values with the browser.
        """
        query_string = environ.get("QUERY_STRING")
        if query_string:
            query_elements = parse_qs(query_string)
            accept = query_elements.get("accept")
            if accept and accept[0]:
                environ["HTTP_ACCEPT"] = accept[0]
        return self.wsgi_app(environ, start_response)
