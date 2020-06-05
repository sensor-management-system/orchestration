import datetime
from calendar import timegm
from functools import wraps
from typing import Dict

import requests
from flask import Blueprint, jsonify, request
from jwkest import JWKESTException
from jwkest.jwk import KEYS
from jwkest.jws import JWS
from project.api.models.base_model import db
from project.api.models.user import User

auth_blueprint = Blueprint('auth', __name__)


class TokenChecker():
    def __init__(self):
        self.config_url: str = \
            'https://webapp-stage.intranet.ufz.de/idp/oidc/v1/' \
            '.well-known/openid-configuration'
        self._load_config()
        self._load_jwks_data()

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
            raise handle_failed_authentication(msg)

    def _validate_claims(self):
        if self.id_token.get('iss') != self.issuer:
            msg = 'Invalid Authorization header. Invalid JWT issuer.'
            raise handle_failed_authentication(msg)

        # Check if token is expired
        utc_timestamp = timegm(datetime.datetime.utcnow().utctimetuple())
        if utc_timestamp > self.id_token.get('exp', 0):
            msg = 'Invalid Authorization header. JWT has expired.'
            raise handle_failed_authentication(msg)
        if 'nbf' in self.id_token and utc_timestamp < self.id_token['nbf']:
            msg = 'Invalid Authorization header. JWT not yet valid.'
            raise handle_failed_authentication(msg)

    def check_token(self, token: str):
        self._decode_token(token=token)
        self._validate_claims()
        return self.id_token


class AuthenticationFailed(Exception):
    status_code = 410

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@auth_blueprint.errorhandler(AuthenticationFailed)
def handle_failed_authentication(error):
    response = jsonify(error)
    # response.status_code = error.status_code
    return response


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
                user = add_user_to_database(current_user)
                get_current_user(user)

            except JWKESTException:
                return jsonify({'message': 'token is invalid'}), 400

            return f(current_user, *args, **kwargs)
        else:
            return f(*args, **kwargs)

    return decorator


def get_current_user(current_user):
    current_user = current_user
    return current_user


def add_user_to_database(current_user):
    exists = db.session.query(User).filter_by(
        subject=current_user['sub']).first()
    if not exists:
        user = User(subject=current_user['sub'])
        db.session.add(user)
        db.session.commit()
        return user
    else:
        return exists


@auth_blueprint.route('/rdm/svm-api/v1/auth', methods=['GET'])
@token_required
def test(current_user):
    response = {
        'status': 'success',
        'message': 'Hello {} from Sensor API!'.format(
            current_user['given_name'])
    }
    return response
