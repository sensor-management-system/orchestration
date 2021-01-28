import json

from flask_jwt_extended import create_access_token
from flask_testing import TestCase

from project import create_app
from project.api.models.base_model import db
from project.api.token_checker import jwt

app = create_app()


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        "sub": identity,
        "email": "test-user@test.de",
        "name": "test user",
        "family_name": "user",
        "given_name": "test",
    }


def create_token():
    hs256_token = create_access_token("testusr@test.de")
    access_headers = {"Authorization": "Bearer {}".format(hs256_token)}
    return access_headers


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
