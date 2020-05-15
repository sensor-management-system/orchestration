from flask_testing import TestCase
from project import create_app
from project.api.models.baseModel import db

app = create_app()


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def set_up(self):
        db.drop_all()
        db.create_all()
        db.session.commit()

    def tear_down(self):
        db.session.remove()
        db.drop_all()
