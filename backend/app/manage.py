# SPDX-FileCopyrightText: 2020 - 2024
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

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
    from project.api.models import (
        Configuration,
        Contact,
        Device,
        ManufacturerModel,
        Platform,
        Site,
    )

    for model_type in [
        Configuration,
        Contact,
        Device,
        ManufacturerModel,
        Platform,
        Site,
    ]:
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


@cli.group()
def b2inst():
    """Group for b2inst sub commands."""
    pass


@b2inst.group("update")
def b2inst_update():
    """Group to update some of the b2inst records."""
    pass


@b2inst_update.command("device")
@click.argument("device_id")
def b2inst_update_device(device_id):
    """Update the b2inst entry for the device with the device_id."""
    from project.api.models import Device
    from project.extensions.instances import pidinst

    entry = db.session.query(Device).filter_by(id=device_id).first()
    pidinst.b2inst.update_external_metadata(entry, run_async=False)


@b2inst_update.command("platform")
@click.argument("platform_id")
def b2inst_update_platform(platform_id):
    """Update the b2inst entry for the platform with the platform_id."""
    from project.api.models import Platform
    from project.extensions.instances import pidinst

    entry = db.session.query(Platform).filter_by(id=platform_id).first()
    pidinst.b2inst.update_external_metadata(entry, run_async=False)


@b2inst_update.command("configuration")
@click.argument("configuration_id")
def b2inst_update_configuration(configuration_id):
    """Update the b2inst entry for the configuration with the configuration_id."""
    from project.api.models import Configuration
    from project.extensions.instances import pidinst

    entry = db.session.query(Configuration).filter_by(id=configuration_id).first()
    pidinst.b2inst.update_external_metadata(entry, run_async=False)


@b2inst_update.command("all")
@click.option(
    "--skip-problematic",
    is_flag=True,
    show_default=True,
    default=False,
    help="Skip the entries that cause problems with the validation on the b2inst side.",
)
def b2inst_update_all(skip_problematic):
    """Update all the entries that have an b2inst record id."""
    from project.api.models import Configuration, Device, Platform
    from project.extensions.instances import pidinst

    b2inst = pidinst.b2inst
    for model_class in [Device, Platform, Configuration]:
        for entry in (
            db.session.query(model_class)
            .filter(model_class.b2inst_record_id.is_not(None))
            .order_by("id")
        ):
            try:
                b2inst.update_external_metadata(entry, run_async=False)
                print(f"Updated {entry} successfully")
            except Exception as e:
                if skip_problematic:
                    print(f"Problem with {entry} - skipping...")
                else:
                    raise e


@cli.group("import")
def import_group():
    """Group some import commands."""
    pass


@import_group.group("manufacturer-models")
def import_manufacturer_models():
    """Group some import commands for manufacturer models."""
    pass


@import_manufacturer_models.command("from-gipp")
def import_manufacturer_models_from_gipp():
    """Import the manufacturer models from GIPP."""
    import requests

    from project.api.models import ManufacturerModel
    from project.api.models.base_model import db

    base_url = "https://gipp.gfz-potsdam.de"
    response = requests.get(f"{base_url}/instrumentcategories.json")
    response.raise_for_status()
    data = response.json()

    def generate_child_elements(data_list):
        for data_entry in data_list:
            if data_entry.get("nodes", []):
                yield from generate_child_elements(data_entry["nodes"])
            else:
                yield data_entry["id"]

    instrument_category_ids_to_import = generate_child_elements(data)

    for id_ in instrument_category_ids_to_import:
        response = requests.get(
            f"{base_url}/instrumentcategories/view/{id_}.json"
        )
        response.raise_for_status()
        data = response.json()
        manufacturer_name = data["Instrumentcategory"]["manufacturer"]
        model = data["Instrumentcategory"]["name"]

        if manufacturer_name and model:
            existing_manufacturer_model = (
                db.session.query(ManufacturerModel)
                .filter_by(manufacturer_name=manufacturer_name, model=model)
                .first()
            )
            if not existing_manufacturer_model:
                new_model = ManufacturerModel(
                    manufacturer_name=manufacturer_name,
                    model=model,
                    external_system_name="GIPP",
                    external_system_url=f"{base_url}/instrumentcategories/view/{id_}",
                )
                db.session.add(new_model)
                db.session.commit()


if __name__ == "__main__":
    cli()
