import os
from functools import wraps

import requests
from flask import Blueprint, request
from flask_jwt_extended import JWTManager, get_raw_jwt, verify_jwt_in_request
from flask_login import LoginManager
from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.models.user import User

auth_blueprint = Blueprint("auth", __name__)
jwt = JWTManager()

OIDC_ISSUER_URL = os.environ.get("WELL_KNOW_URL")

# retrieve master openid-configuration endpoint for issuer realm
oidc_config = requests.get(OIDC_ISSUER_URL, verify=False).json()
# retrieve data from jwks_uri endpoint
oidc_jwks_uri = requests.get(oidc_config["jwks_uri"], verify=False).json()

login_manager = LoginManager()


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.method != "GET":
            verify_jwt_in_request()
        return fn(*args, **kwargs)

    return wrapper


@jwt.user_loader_callback_loader
def add_user_to_database(current_user):
    exists = db.session.query(User).filter_by(subject=current_user).first()
    if not exists:
        given_name = get_raw_jwt()["given_name"]
        family_name = get_raw_jwt()["family_name"]
        email = get_raw_jwt()["email"]
        subject = get_raw_jwt()["sub"]
        contact = Contact(given_name=given_name, family_name=family_name, email=email)
        db.session.add(contact)
        db.session.commit()
        user = User(subject=subject, contact_id=contact.id)
        db.session.add(user)
        db.session.commit()
        return user
    return exists


@auth_blueprint.route("/rdm/svm-api/v1/auth", methods=["GET"])
@token_required
def test():
    """Just to test the functionality of the JWT encoding.

    :param current_user: JWT
    :return: dict
    """
    response = {
        "status": "success",
        "message": "Hello {} from Sensor API!".format(get_raw_jwt()["given_name"]),
    }
    return response
