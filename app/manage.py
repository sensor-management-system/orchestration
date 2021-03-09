import unittest

import coverage
from flask.cli import FlaskGroup

from project import create_app
from project.api.models.base_model import db
from project.tests import suite

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
def test():
    """ Runs the tests without code coverage """
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())


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


@cli.group()
def es():
    """Group for elasticsearch so that the sub commands are grouped there."""
    pass


@es.command("reindex")
def es_reindex():
    """Reindex all of the models that should be used in the es."""
    from project.api.models.configuration import Configuration
    from project.api.models.device import Device
    from project.api.models.platform import Platform
    from project.api.models.contact import Contact

    for model_type in [Platform, Device, Configuration, Contact]:
        model_type.reindex()


@app.after_request
def add_header(response):
    return response


if __name__ == "__main__":
    cli()
