"""Module that defines a token_required decorator."""

from functools import wraps

from flask import request

from .helpers.errors import UnauthorizedError
from .models import Contact, User
from .models.base_model import db


def token_required(fn):
    """Make sure that we have a valid token before executing a views code."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        """Wrap the function & check for the token before."""
        if request.method not in ["GET", "HEAD", "OPTION"]:
            if not request.user:
                # In this wrapper we can't use the error handler
                # for this kind of error response, so we will
                # return the payload right away.
                return UnauthorizedError(
                    "Write access requires authentication."
                ).respond()
        return fn(*args, **kwargs)

    return wrapper
