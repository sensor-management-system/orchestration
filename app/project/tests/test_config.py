import os
import unittest

from flask import current_app
from flask_testing import TestCase
from project import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    """
    Test Development Config
    """

    def create_app(self):
        """

        :return:
        """
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        """

        :return:
        """
        self.assertTrue(app.config['SECRET_KEY'] == 'top_secret')
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')
        )


class TestTestingConfig(TestCase):
    """
    Test Testing Config
    """

    def create_app(self):
        """

        :return:
        """
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        """

        :return:
        """
        self.assertTrue(app.config['SECRET_KEY'] == 'top_secret')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_TEST_URL')
        )


class TestProductionConfig(TestCase):
    """
    Test Production Config
    """

    def create_app(self):
        """

        :return:
        """
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        """

        :return:
        """
        self.assertTrue(app.config['SECRET_KEY'] == 'top_secret')
        self.assertFalse(app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
