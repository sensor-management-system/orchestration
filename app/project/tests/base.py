import json
import os
import time

from faker import Faker
from flask_jwt_extended import create_access_token
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


class BaseTestCase(TestCase):
    """Base test case for all testing the code of our app."""

    def create_app(self):
        """
        Create the flask app - with test settings.

        :return: flask app object
        """
        app.config.from_object("project.config.TestingConfig")
        app.elasticsearch = None
        return app

    def setUp(self):
        """
        Set up for all the tests.

        Clear the database & mock the authentification for all of our tests.
        :return: None
        """
        db.drop_all()
        db.create_all()
        db.session.commit()

        self.original_verify_valid_access_token_in_request = (
            open_id_connect.__class__._verify_valid_access_token_in_request
        )

        def verify_valid_access_token_for_tests(self):
            """Fake the verification for our tests."""
            # We don't ask the user info endpoint, we just use data
            # decoded from the token.
            # Sub will be the identity.
            attributes = generate_userinfo_data()
            identity = attributes["sub"]
            return identity, attributes

        open_id_connect.__class__._verify_valid_access_token_in_request = (
            verify_valid_access_token_for_tests
        )

    def tearDown(self):
        """
        Cleanup after the tests.

        Drop all the content of the database & restore our
        authentification mechanism.
        :return:
        """
        db.session.remove()
        db.drop_all()

        open_id_connect.__class__._verify_valid_access_token_in_request = (
            self.original_verify_valid_access_token_in_request
        )

    def add_object(self, url, data_object, object_type):
        """Ensure a new object can be added to the database."""
        with self.client:
            response = self.client.post(
                url,
                data=json.dumps(data_object),
                content_type="application/vnd.api+json",
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn(object_type, data["data"]["type"])
        return data

    def add_object_invalid_data_key(self, url, data_object):
        """Ensure error is thrown if the JSON object has invalid data key."""
        with self.client:
            response = self.client.post(
                url=url,
                data=json.dumps(data_object),
                content_type="application/vnd.api+json",
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Not a valid string.", data["errors"][0]["detail"])

    def update_object(self, url, data_object, object_type):
        """Ensure a old object can be updated."""
        with self.client:
            response = self.client.patch(
                url,
                data=json.dumps(data_object),
                content_type="application/vnd.api+json",
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn(object_type, data["data"]["type"])
        return data

    def delete_object(self, url):
        """Ensure delete an object."""
        with self.client:
            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Object successfully deleted", data["meta"]["message"])
        return data

    def http_code_404_when_resource_not_found(self, url):
        """Ensure that the backend respond with 404 if resource not found."""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
