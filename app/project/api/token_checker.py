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
            open_id_connect.verify_valid_access_token_in_request_and_set_user()
        return fn(*args, **kwargs)

    return wrapper


@open_id_connect.user_lookup_loader
def add_user_to_database(identity, user_info_data):
    """
    Load the user from the database.

    Also create the user if necessary.
    """
    current_user_exists = (
        db.session.query(User).filter_by(subject=identity).one_or_none()
    )

    if not current_user_exists:
        given_name = user_info_data["given_name"]
        family_name = user_info_data["family_name"]
        email = user_info_data["email"]
        subject = identity
        current_contact_exists = (
            db.session.query(Contact).filter_by(email=email).first()
        )
        contact = add_contact_if_not_exists(
            current_contact_exists, email, family_name, given_name
        )
        user = User(subject=subject, contact_id=contact.id)
        db.session.add(user)
        db.session.commit()
        return user
    elif not current_user_exists.active:
        raise ForbiddenError(
            "This user is deactivated. Please contact your admin in order to reactivate the user."
        )
    return current_user_exists


def add_contact_if_not_exists(current_contact_exists, email, family_name, given_name):
    """Create the contact if it is not in the database so far."""
    if not current_contact_exists:
        contact = Contact(given_name=given_name, family_name=family_name, email=email)
        db.session.add(contact)
        db.session.commit()
        return contact
    return current_contact_exists


def current_user_or_none(optional=False):
    """Verify access token and get current user if token is given
    or return None."""
    try:
        open_id_connect.verify_valid_access_token_in_request_and_set_user()
        current_user = open_id_connect.get_current_user()
        return current_user
    except (UnauthorizedError, AttributeError):
        if optional:
            return None
        else:
            raise UnauthorizedError("No valid access token.")
