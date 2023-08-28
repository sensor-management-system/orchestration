# SPDX-FileCopyrightText: 2020 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Module that defines a token_required decorator."""

from functools import wraps

from flask import request, g

from .helpers.errors import UnauthorizedError
from .models import Contact, User
from .models.base_model import db


def token_required(fn):
    """Make sure that we have a valid token before executing a views code."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        """Wrap the function & check for the token before."""
        if request.method not in ["GET", "HEAD", "OPTION"]:
            if not g.user:
                # In this wrapper we can't use the error handler
                # for this kind of error response, so we will
                # return the payload right away.
                return UnauthorizedError("Authentication required.").respond()
        return fn(*args, **kwargs)

    return wrapper
