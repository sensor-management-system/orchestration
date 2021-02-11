from functools import wraps

from flask import request
from flask_jwt_extended import JWTManager, get_raw_jwt, verify_jwt_in_request

from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.models.user import User

jwt = JWTManager()


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.method != "GET":
            verify_jwt_in_request()
        return fn(*args, **kwargs)

    return wrapper


@jwt.user_loader_callback_loader
def add_user_to_database(current_user):
    current_user_exists = db.session.query(User).filter_by(subject=current_user).first()

    if not current_user_exists:
        raw_jwt_object = get_raw_jwt()
        given_name = raw_jwt_object["given_name"]
        family_name = raw_jwt_object["family_name"]
        email = raw_jwt_object["email"]
        subject = raw_jwt_object["sub"]
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
    return current_user_exists


def add_contact_if_not_exists(current_contact_exists, email, family_name, given_name):
    if not current_contact_exists:
        contact = Contact(given_name=given_name, family_name=family_name, email=email)
        db.session.add(contact)
        db.session.commit()
        return contact
    return current_contact_exists
