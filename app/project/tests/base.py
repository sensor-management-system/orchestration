import json

from flask_testing import TestCase
from project import create_app
from project.api.models.base_model import db

app = create_app()


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
        """Ensure error is thrown if the JSON object
        has invalid data key."""

        with self.client:
            response = self.client.post(
                url=url,
                data=json.dumps(data_object),
                content_type="application/vnd.api+json",
            )

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.assertIn("Not a valid string.", data["errors"][0]["detail"])
