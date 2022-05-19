"""Base class & utils for the tests."""

import json
import os
import time
from contextlib import contextmanager

import flask_jwt_extended
from faker import Faker
from flask import request
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTDecodeError, WrongTokenError
from flask_testing import TestCase
from jwt.exceptions import DecodeError

from project import create_app
from project.api.helpers.errors import UnauthorizedError
from project.api.models.base_model import db
from project.extensions.auth.mechanisms.mixins import CreateNewUserByUserinfoMixin
from project.extensions.instances import auth

app = create_app()
jwt = JWTManager(app)
fake = Faker()

test_file_path = os.path.abspath(os.path.dirname(__file__))


def query_result_to_list(query_result):
    """
    Convert a query result to a list.

    Query results from sqlalchemy are ok to work with
    (so for further filtering, to retrieve the length, etc.)
    as they are lazy.

    However sometimes it is easier to deal with them as
    simple plain python lists - this is what this utility function
    here does.
    """
    return [r for r in query_result]


def generate_userinfo_data():
    """
    Generate jwt payload data.

    :return: identity & payload

        :Example:
            {
              "iat": 1612259403,
              "sub": "jasonmcp@unittest.test",
              "iss": "SMS unittest",
              "name": "Jason Mcpherson",
              "family_name": "mcpherson",
              "given_name": "jason",
              "email": "jason.mcpherson@unittest.test",
              "exp": 1612259463,
              "aud": "SMS"
            }
    """
    # get current time in seconds
    now = int(time.time())
    # generate a random name will bw like "test test"
    name = fake.unique.name()
    # separate the name to a list
    name_l = name.lower().split(" ")
    family_name = name_l[1]
    given_name = name_l[0]
    # Should be like the sub which comes from the IDP
    identity = f"{''.join(name_l)[:8]}@unittest.test"
    token_data = {
        "sub": identity,
        "iss": "SMS unittest",
        "name": name,
        "family_name": family_name,
        "given_name": given_name,
        "email": fake.unique.email(),
        "iat": now,  # Issued At: Date/time when the token was issued
        "exp": now + 60,  # Expiration: expire after one minute.
        "aud": "SMS",  # recipient of this token
    }
    return token_data


def create_token(attributes=None):
    """
    create a JWT token.

    :param attributes: specified token attributes
    :return: authorization header as string
    """
    if not attributes:
        attributes = generate_userinfo_data()
    identity = attributes["sub"]
    token = flask_jwt_extended.create_access_token(
        identity=identity, additional_claims=attributes
    )
    return {"Authorization": "{}".format(token)}


def get_userinfo():
    """
    Decode the JWT instead of asking the user-info.

    :return: a dictionary with user attributes.
    """
    authorization_header = request.headers.get("Authorization")
    try:
        decode_token = flask_jwt_extended.decode_token(authorization_header)
        return decode_token
    except Exception as e:
        # In case we have a problem with the decoding.
        raise UnauthorizedError(repr(e))


class LoginMechanismBySettingUserDirectly:
    def __init__(self, get_user_function):
        self.get_user_function = get_user_function

    def init_app(self, app):
        pass

    @staticmethod
    def can_be_applied():
        return True

    def authenticate(self):
        fun = self.get_user_function
        user = fun()
        return user


class LoginMechanismByTestJwt(CreateNewUserByUserinfoMixin):
    def init_app(self, app):
        pass

    @staticmethod
    def can_be_applied():
        if request.headers.get("Authorization"):
            return True
        return False

    def authenticate(self):
        authorization_header = request.headers.get("Authorization")
        try:
            decode_token = flask_jwt_extended.decode_token(authorization_header)
            identity = decode_token["sub"]
            return self.get_user_or_create_new(identity, decode_token)
        except (ValueError, DecodeError, TypeError, WrongTokenError):
            return None


class BaseTestCase(TestCase):
    """Base test case for all testing the code of our app."""

    def create_app(self):
        """
        Create the flask app - with test settings.

        :return: flask app object
        """
        app.config.from_object("project.config.TestingConfig")
        app.elasticsearch = None
        # We support 2 mechanisms for testing:
        # One is that we just reuse the existing Jwt tokens that we already have.
        # Or we just have a force_login method in the test, so that we can enforce
        # that we are a certain user (if the mechanism itself doesn't matter).
        auth.mechanisms = [
            LoginMechanismByTestJwt(),
            LoginMechanismBySettingUserDirectly(self.get_current_user),
        ]
        return app

    def force_login(self, user):
        self._base_test_current_user = user

    def logout(self):
        self._base_test_current_user = None

    def get_current_user(self):
        return self._base_test_current_user

    @contextmanager
    def run_requests_as(self, user):
        previous_user = self._base_test_current_user
        self._base_test_current_user = user
        try:
            yield
        finally:
            self._base_test_current_user = previous_user

    def setUp(self):
        """
        Set up for all the tests.

        Clear the database & mock the authentification for all of our tests.
        :return: None
        """
        db.drop_all()
        db.create_all()
        db.session.commit()

        # We start every test without being logged in
        self.logout()

    def tearDown(self):
        """
        Cleanup after the tests.

        Drop all the content of the database & restore our
        authentication mechanism.
        :return:
        """
        db.session.remove()
        db.drop_all()

        self.logout()

    def add_object(self, url, data_object, object_type):
        """Ensure a new object can be added to the database."""
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                url,
                data=json.dumps(data_object),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn(object_type, data["data"]["type"])
        return data

    def add_object_invalid_data_key(self, url, data_object):
        """Ensure error is thrown if the JSON object has invalid data key."""
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                url=url,
                data=json.dumps(data_object),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Not a valid string.", data["errors"][0]["detail"])

    def update_object(self, url, data_object, object_type):
        """Ensure an old object can be updated."""
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                url,
                data=json.dumps(data_object),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn(object_type, data["data"]["type"])
        return data

    def delete_object(self, url):
        """Ensure delete an object."""
        access_headers = create_token()
        with self.client:
            response = self.client.delete(
                url, content_type="application/vnd.api+json", headers=access_headers
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Object successfully deleted", data["meta"]["message"])
        return data

    def http_code_404_when_resource_not_found(self, url):
        """Ensure that the backend respond with 404 if resource not found."""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
