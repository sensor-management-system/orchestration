# SPDX-FileCopyrightText: 2020 - 2023
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""CLI commands for the flask maange.py."""

import json
import pathlib
import sys
import unittest

import click
import coverage
from flask.cli import FlaskGroup

from project import create_app
from project.api.helpers.errors import ErrorResponse
from project.api.models import Contact, User
from project.api.models.base_model import db
from project.api.services.userservice import user_deactivation

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    """Short command to completely recreate the database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
@click.argument("test_names", nargs=-1)
def test(test_names):
    """Run the tests without code coverage."""
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
@click.argument("test_names", nargs=-1)
def cov(test_names):
    """Run the unit tests with coverage."""
    coverage_ = coverage.coverage(
        branch=True,
        include="project/*",
        # skip the tests itself for the coverage
        omit=[
            "project/tests/*",
            "project/config.py",
        ],
    )
    coverage_.erase()
    coverage_.start()

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
        coverage_.stop()
        coverage_.save()
        click.secho("Coverage Summary:", fg="green")
        # coverage_.html_report(directory="coveragereport", skip_empty=True)
        coverage_.report(
            show_missing=True,
            skip_empty=True,
            skip_covered=True,
        )
        return sys.exit(0)
    return sys.exit(1)


@cli.group()
def es():
    """Group for elasticsearch so that the sub commands are grouped there."""
    pass


@es.command("reindex")
def es_reindex():
    """Reindex all the models that should be used in the es."""
    from project.api.models import Configuration, Contact, Device, Platform, Site

    for model_type in [Platform, Device, Configuration, Contact, Site]:
        model_type.reindex()


@app.after_request
def add_header(response):
    """Add some headers if needed."""
    return response


@app.errorhandler(ErrorResponse)
def handle_exception(error: ErrorResponse):
    """Add an overall error hanlder for the flask rest json error responses."""
    return error.respond()


@cli.group()
def users():
    """Group for user command so that the sub commands are grouped there."""
    pass


@users.command("deactivate")
@click.argument("src_user_subject")
@click.option("--dest-user-subject", default=None, help="A substituted user subject")
def deactivate_a_user(src_user_subject, dest_user_subject):
    """
    Deactivate a user.

    Take the following steps:
     - Set the active attribute to False
     - Replace contact entities with a deactivation message.
     - If a there is substituted user then add it to all objects where
       the deactivated user is listed.

    # How to use:
    python manage.py users deactivate srcuserubject@ufz.de --dest-user-subject=destusersubject@ufz.de

    :param src_user_subject: Subject attribute for the user Intended to be deactivated.
    :param dest_user_subject: Subject attribute for the substituted user.
    """
    src_user = db.session.query(User).filter_by(subject=src_user_subject).first()
    if not src_user:
        raise click.BadParameter(
            f"Can't find a user with subject {src_user_subject} to deactivate"
        )
    src_contact = src_user.contact

    dest_contact = None
    if dest_user_subject is not None:
        dest_user = db.session.query(User).filter_by(subject=dest_user_subject).first()
        if not dest_user:
            raise click.BadParameter(
                f"Can't find a user with subject {dest_user_subject} for substituion"
            )
        dest_contact = (
            db.session.query(Contact).filter_by(id=dest_user.contact_id).first()
        )

    user_deactivation(src_user, src_contact, dest_contact)


@users.command("reactivate")
@click.argument("subject_user")
@click.option("--given_name", prompt="Contact given_name please")
@click.option("--family_name", prompt="Contact family_name please")
@click.option("--email", prompt="Contact email please")
def reactivate_a_user(subject_user, given_name, family_name, email):
    """
    Reactivate a user.

    The user active attribute will be set to True and then the contact
    Info will be asked by Prompting.

    # How to use:
     python manage.py users deactivate srcuserubject@ufz.de


    :param subject_user: Subject attribute for the user.
    :param given_name: Contact given name.
    :param family_name: Contact family name.
    :param email: Contact email.
    """
    user = db.session.query(User).filter_by(subject=subject_user).first()
    contact = db.session.query(Contact).filter_by(id=user.contact_id).first()

    contact.active = True
    contact.given_name = given_name
    contact.family_name = family_name
    contact.email = email
    contact.website = None
    contact.orcid = None
    contact.organization = ""

    user.active = True

    db.session.commit()


@users.command("upgrade-to-superuser")
@click.argument("user_subject")
def make_super_user(user_subject):
    """
    Upgrade a user to superuser a superuser.

    How To use: python manage.py users upgrade-to-superuser testuser@ufz.de

    :param user_subject: the subject attribute identical to jwt.sub
    """
    user = db.session.query(User).filter_by(subject=user_subject).first()
    user.is_superuser = True
    db.session.commit()
    click.secho(f"{user.contact.given_name} is now upgraded to super user!", fg="green")
    click.secho(
        "As super-user you will be able to modify or delete any entity \n"
        "in SMS without the need to belong to a group or a project.\n"
        "Please use it wisely",
        fg="yellow",
    )


@users.command("downgrade-to-user")
@click.argument("user_subject")
def downgrade_to_user(user_subject):
    """
    Downgrade a superuser to a normal user.

    How To use: python manage.py users downgrade-to-user testsuperuser@ufz.de

    :param user_subject: the subject attribute identical to jwt.sub
    """
    user = db.session.query(User).filter_by(subject=user_subject).first()
    user.is_superuser = False
    db.session.commit()
    click.secho(
        f"{user.contact.given_name} is now a downgraded to a normal user!", fg="green"
    )


@cli.command("loaddata")
@click.argument("fixture_file")
@click.option(
    "-m",
    "--skip-missing-file",
    is_flag=True,
    show_default=True,
    default=False,
    help="Skip if the file is missing.",
)
@click.option(
    "-e",
    "--skip-empty-file",
    is_flag=True,
    show_default=True,
    default=False,
    help="Skip if the file is empty.",
)
def loaddata(fixture_file, skip_missing_file, skip_empty_file):
    """
    Load data from a json fixture file into the database.

    Should mimik the behaviour of the django loaddata command,
    but uses Model names ("TsmEndpoint") instead of the django
    like table names that are composed by app & plural name
    ("app_tsm_endpoints").
    """
    from project.api import models

    path = pathlib.Path(fixture_file)

    # Same fast tests to ensure we can skip loading the data.
    if skip_missing_file and not path.exists():
        return
    if skip_empty_file and path.stat().st_size == 0:
        return

    # Read the file
    with path.open() as infile:
        # Only support for json files.
        entries = json.load(infile)
    # And put the entries in the database.
    for entry in entries:
        model = getattr(models, entry["model"])
        existing_entry = db.session.get(model, entry["pk"])
        if existing_entry:
            for key, value in entry["fields"].items():
                setattr(existing_entry, key, value)
            db.session.add(existing_entry)
        else:
            new_entry = model(**entry["fields"])
            # No support for composed primary keys at the moment.
            pk = model.__mapper__.primary_key[0].name
            setattr(new_entry, pk, entry["pk"])
            db.session.add(new_entry)
    db.session.commit()


@cli.command("openapi")
def openapi():
    """Dump the openapi spec file."""
    from project.views.docs import openapi_json

    answer = openapi_json()
    openapi_text = answer[0]
    print(openapi_text)


if __name__ == "__main__":
    cli()
