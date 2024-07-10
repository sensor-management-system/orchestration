# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Utility functions for our plain flask views."""

import functools

from flask_rest_jsonapi.exceptions import JsonApiException

from ..api.helpers.errors import ErrorResponse


def handle_json_api_errors(f):
    """Wrap the function so that we can throw exceptions."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            return result
        except ErrorResponse as e:
            return e.respond()
        except JsonApiException as e:
            return e.to_dict(), e.status

    return wrapper
