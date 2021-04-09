import json
import os
import time

from faker import Faker
from flask_jwt_extended.tokens import _encode_jwt
from flask_testing import TestCase

from project import create_app
from project.api.models.base_model import db

app = create_app()
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


def encode_token_date_with_hs256(
    token_data,
    headers=None,
):
    """
    Make use of the flask_jwt_extended methode (_encode_jwt) to
    encode our payload.
    The test uses "HS256" as encode algorithm.

    :param token_data:
    :param identity: Identifier for who this token is for (ex, sub).
    :param fresh: this will indicate how long this
                  token will remain fresh.
    :param expires_delta: How far in the future this token should expire
    :param headers:
    :return:
    """
    return _encode_jwt(
        token_data,
        expires_delta=None,
        secret=app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
        json_encoder=None,
        headers=headers,
    )


def create_token():
    """
    Mock a 'HS256' jwt same to the one, that come from idp
     and prepare the access header.

    :return: an access token dict for the request headers
    """
    token_data = generate_token_data()
    hs256_token = encode_token_date_with_hs256(token_data)
    access_headers = {"Authorization": "Bearer {}".format(hs256_token)}
    return access_headers


def generate_token_data():
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


class BaseTestCase(TestCase):
    """
    Base Test Case
    """

    def create_app(self):
        """

        :return:
        """
        app.config.from_object("project.config.TestingConfig")
        app.elasticsearch = None
        return app

    def setUp(self):
        """

        :return:
        """
        db.drop_all()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        """

        :return:
        """
        db.session.remove()
        db.drop_all()

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
        """Ensure error is thrown if the JSON object
        has invalid data key."""

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
        """Ensure a old object can be updated."""
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
                url,
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Object successfully deleted", data["meta"]["message"])
        return data
