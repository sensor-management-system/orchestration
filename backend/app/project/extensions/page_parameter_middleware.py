# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Middleware to handle page parameters for the JSON:API."""
from flask import request

from ..api.helpers.errors import BadRequestError


class PageParameterMiddleware:
    """
    Middleware to handle page parameters.

    As the JSON:API handling is mostly encapsulated within the
    flask_rest_jsonapi library, we can't change the code directly.
    Howver, we can register middlewares that catch this kind of problems
    if we have invalid parameters for page size or page number.
    """

    def __init__(self, app=None):
        """Init the object with the app."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Register the middleware functions."""
        app.before_request(self.check_page_parameters)

    def check_page_parameters(self):
        """Return 400 responses if we run into problems with our page parameters."""
        if "page[size]" in request.args.keys():
            value_str = request.args["page[size]"]
            value_int = int(value_str)
            if value_int < 0:
                return BadRequestError("page[size] can not be negative").respond()
        if "page[number]" in request.args.keys():
            value_str = request.args["page[number]"]
            value_int = int(value_str)
            if value_int < 1:
                return BadRequestError(
                    "page[number] can not be negative or zero"
                ).respond()
