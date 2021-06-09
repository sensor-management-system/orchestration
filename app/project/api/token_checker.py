from functools import wraps

from flask import request, current_app
from flask_jwt_extended import JWTManager, get_raw_jwt, verify_jwt_in_request

from .models import Contact, User
from .models.base_model import db

jwt = JWTManager()


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.method != "GET":
            try:
                verify_jwt_in_request()
            except:
                # In case that our verification fails, it may be due to
                # an old jwt public key (idp may have changes in the meantime)
                # So we want to reload our config and test if again
                if current_app.config["OIDC_JWT_SERVICE"] is not None:
                    oidc_jwt_service = current_app.config["OIDC_JWT_SERVICE"]
                    # The service is cached by itself, so we don't run queries all the time
                    current_app.config[
                        "JWT_PUBLIC_KEY"
                    ] = oidc_jwt_service.get_jwt_public_key()
                    current_app.config[
                        "JWT_ALGORITHM"
                    ] = oidc_jwt_service.get_jwt_algorithm()

            # if it fails again, then we don't want to allow the user to use the endpoint
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
