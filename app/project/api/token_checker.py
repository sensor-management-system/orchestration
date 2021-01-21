import datetime
import os
from calendar import timegm
from functools import wraps
from typing import Dict

import requests
from flask import Blueprint, jsonify, request
from flask_rest_jsonapi.exceptions import AccessDenied
from jwkest import JWKESTException
from jwkest.jwk import KEYS
from jwkest.jws import JWS
from project.api.models.base_model import db
from project.api.models.user import User

auth_blueprint = Blueprint('auth', __name__)

current_user_id = None


class TokenChecker():
    def __init__(self):
        self.config_url: str = os.environ.get('WELL_KNOW_URL')
        self._load_config()
        self._load_jwks_data()
        self.id_token = None

    def __str__(self):
        return ": email %s" % (self.id_token['sub'])

    def _load_config(self):
        # Loads issuer and jwks url
        self.oidc_config: Dict = requests.get(
            self.config_url, verify=True).json()
        self.issuer = self.oidc_config['issuer']

    def _load_jwks_data(self):
        # jwks data contains the key you need to extract the token
        self.jwks_keys: KEYS = KEYS()
        self.jwks_keys.load_from_url(self.oidc_config['jwks_uri'])

    def _decode_token(self, token: str):
        try:
            self.id_token = JWS().verify_compact(token, keys=self.jwks_keys)
        except JWKESTException:
            msg = 'Invalid Authorization header. ' \
                  'JWT Signature verification failed'
            raise AccessDenied(msg)

    def _validate_claims(self):
        if self.id_token.get('iss') != self.issuer:
            msg = 'Invalid Authorization header. Invalid JWT issuer.'
            raise AccessDenied(msg)

        # Check if token is expired
        utc_timestamp = timegm(datetime.datetime.utcnow().utctimetuple())
        if utc_timestamp > self.id_token.get('exp', 0):
            msg = 'Invalid Authorization header. JWT has expired.'
            raise AccessDenied(msg)
        if 'nbf' in self.id_token and utc_timestamp < self.id_token['nbf']:
            msg = 'Invalid Authorization header. JWT not yet valid.'
            raise AccessDenied(msg)

    def check_token(self, token: str):
        self._decode_token(token=token)
        self._validate_claims()
        return self.id_token


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not request.method == 'GET':
            token = None

            if 'token' in request.headers:
                token = request.headers['token']

            if not token:
                return jsonify({'message': 'a valid token is missing'}), 400

            try:
                current_user = TokenChecker().check_token(token=token)
                u = add_user_to_database(current_user)
                global current_user_id
                current_user_id = u
            except JWKESTException:
                return jsonify({'message': 'token is invalid'}), 400

            return f(current_user, *args, **kwargs)
        else:
            return f(*args, **kwargs)

    return decorator


def add_user_to_database(current_user):
    exists = db.session.query(User).filter_by(
        subject=current_user['sub']).first()
    if not exists:
        given_name = current_user['given_name']
        family_name = current_user['family_name']
        email = current_user['email']
        subject = current_user['sub']
        from project.api.models.contact import Contact
        contact = Contact(given_name=given_name, family_name=family_name,
                          email=email)
        db.session.add(contact)
        db.session.commit()
        user = User(subject=subject, contact_id=contact.id)
        db.session.add(user)
        db.session.commit()
        return user.id
    return exists.id


@auth_blueprint.route('/rdm/svm-api/v1/auth', methods=['GET'])
@token_required
def test(current_user):
    """Just to test the functionality of the JWT encoding.

    :param current_user: JWT
    :return: dict
    """
    response = {
        'status': 'success',
        'message': 'Hello {} from Sensor API!'.format(
            current_user['given_name'])
    }
    return response
