import unittest

import coverage
from flask.cli import FlaskGroup
from project import create_app
from project.api.insert_initial_values import *
from project.api.models.base_model import db
from project.tests.base import BaseTestCase

app = create_app()
cli = FlaskGroup(create_app=create_app)

COV = coverage.coverage(
    branch=True, include="project/*", omit=["project/tests/*", "project/config.py",]
)
COV.start()


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Runs the tests without code coverage """
    tests = unittest.TestLoader().discover("project/tests", pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover("project/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
    COV.save()
    print("Coverage Summary:")
    COV.report()
    COV.html_report()
    COV.erase()
    return 0
    return 1


@cli.command("db_init")
def db_init():
    with app.app_context():
        device = add_device()
        event = add_event(device)
        contact = add_contact()
        platform = add_platform()
        attachment = add_device_attachment(device)
        pl_attachment = add_platform_attachment(platform)
        db.session.add(device)
        db.session.add(platform)
        db.session.add(event)
        db.session.add(contact)
        db.session.add(attachment)
        db.session.add(pl_attachment)
        db.session.commit()


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://git.ufz.de'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

    return response


if __name__ == "__main__":
    cli()
