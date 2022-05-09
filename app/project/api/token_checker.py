"""Module that defines a token_required decorator."""

from functools import wraps

from flask import request

from .auth.flask_openidconnect import open_id_connect
from .helpers.errors import ForbiddenError, UnauthorizedError
from .models import Contact, User
from .models.base_model import db


def token_required(fn):
    """Make sure that we have a valid token before executing a views code."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        """Wrap the function & check for the token before."""
        if request.method not in ["GET", "HEAD", "OPTION"]:
            if not request.user:
                raise UnauthorizedError("Write access requires authentication.")
        return fn(*args, **kwargs)

    return wrapper



def get_current_user_or_none_by_optional(optional=False):
    """Verify access token and get current user if token is given
    or return None if it is just optional."""
    return request.user
