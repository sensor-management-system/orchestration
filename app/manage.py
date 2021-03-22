import sys
import unittest

import click
import coverage
from flask.cli import FlaskGroup

from project import create_app
from project.api.models.base_model import db

app = create_app()
cli = FlaskGroup(create_app=create_app)

COV = coverage.coverage(
    branch=True,
    include="project/*",
    # skip the tests itself for the coverage
    omit=[
        "project/tests/*",
        "project/config.py",
    ],
)
COV.start()


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """ Runs the tests without code coverage """
    # To run an oly test just pass th test-model-name
    # an example:
    # "python manage.py test project.tests.api.test_platform_software_update_action_attachment"
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover(
            "project/tests",
            # Only execute the files starting with test_
            # as we have some helper files here as well.
            pattern="test_*.py",
        )
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return sys.exit(0)
    return sys.exit(1)


@cli.command()
@click.argument('test_names', nargs=-1)
def cov(test_names):
    """Runs the unit tests with coverage."""
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover(
            "project/tests",
            # Only execute the files starting with test_
            # as we have some helper files here as well.
            pattern="test_*.py",
        )
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        return sys.exit(0)
    return sys.exit(1)


@cli.group()
def es():
    """Group for elasticsearch so that the sub commands are grouped there."""
    pass


@es.command("reindex")
def es_reindex():
    """Reindex all of the models that should be used in the es."""
    from project.api.models import (Configuration, Device, Platform, Contact)

    for model_type in [Platform, Device, Configuration, Contact]:
        model_type.reindex()


@app.after_request
def add_header(response):
    return response


if __name__ == "__main__":
    cli()
