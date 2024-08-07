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
import os
import pathlib
import sys
import unittest

import click
import coverage
import requests
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

    In most cases it makes sense to have a `pk` element given,
    so that we can insert/update based on a primary key (mostly the id).

    But we can also consider a combination of fields to be unique.
    with

    unique: ["label"]

    We can update the fields based on the value of the `label` entry.

    Another option is to use references for entries that were previously
    inserted/updated.

    [
      {
        "model": "ManufacturerModel",
        "unique": ["manufacturer_name", "model"],
        "fields": {
          "manufacturer_name": "GFZ",
          "model": "custom"
        },
        "result": "gfz_entry"
      },
      {
        "model": "ExportControl",
        "unique": ["manufacturer_model"],
        "references": {
          "manufacturer_model": "gfz_entry"
        },
        "fields": {
          "dual_use": false
        }
      }
    ]

    result defines the name that we can use to reference the entry later, while
    references lets us use the concrete value for a field.
    This way we can set foreign key values.
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
        fixture_list_entries = json.load(infile)
    # And put the entries in the database.
    reference_table = {}

    def set_fields(db_entry, fixture_list_entry):
        for field_name, value in fixture_list_entry["fields"].items():
            setattr(db_entry, field_name, value)
        for field_name, reference_key in fixture_list_entry.get(
            "references", {}
        ).items():
            setattr(db_entry, field_name, reference_table[reference_key])

    for fixture_list_entry in fixture_list_entries:
        model = getattr(models, fixture_list_entry["model"])
        # If we have a primary key, everything is easy.
        pk_value = fixture_list_entry.get("pk")
        unique = fixture_list_entry.get("unique")
        stored_db_entry = None
        if pk_value:
            existing_db_entry = db.session.get(model, pk_value)
            if existing_db_entry:
                set_fields(existing_db_entry, fixture_list_entry)
                db.session.add(existing_db_entry)
                stored_db_entry = existing_db_entry
            else:
                new_db_entry = model()
                set_fields(new_db_entry, fixture_list_entry)
                # No support for composed primary keys at the moment.
                pk_field = model.__mapper__.primary_key[0].name
                setattr(new_db_entry, pk_field, pk_value)
                db.session.add(new_db_entry)
                stored_db_entry = new_db_entry
        elif unique:
            # If we don't have the id (because we might don't know), we still want
            # to be able to insert or update based on a unique setting.
            # (So we could overwrite data based on a name attribute).
            query = db.session.query(model)

            for key in unique:
                if key in fixture_list_entry["fields"].keys():
                    value = fixture_list_entry["fields"][key]
                elif key in fixture_list_entry["references"].keys():
                    value = reference_table[fixture_list_entry["references"][key]]
                filter_dict = {key: value}
                query = query.filter_by(**filter_dict)
            count_of_existing_db_entries = query.count()
            if count_of_existing_db_entries not in [0, 1]:
                raise Exception(f"Not unique for {fixture_list_entry}")
            existing_db_entry = query.first()
            if existing_db_entry:
                set_fields(existing_db_entry, fixture_list_entry)
                db.session.add(existing_db_entry)
                stored_db_entry = existing_db_entry
            else:
                new_db_entry = model()
                set_fields(new_db_entry, fixture_list_entry)
                db.session.add(new_db_entry)
                stored_db_entry = new_db_entry

        if stored_db_entry:
            if fixture_list_entry.get("result"):
                reference_table[fixture_list_entry["result"]] = stored_db_entry

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
        response = requests.get(f"{base_url}/instrumentcategories/view/{id_}.json")
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


@cli.group("cv")
@click.pass_context
def cv_group(ctx):
    """Group for commands that are related to the controlled vocabulary."""
    from project.api import models

    ctx.ensure_object(dict)
    ctx.obj["fields_to_check"] = [
        (models.ConfigurationContactRole, {"role_uri": "role_name"}),
        (
            models.ConfigurationParameter,
            {
                "unit_uri": "unit_name",
            },
        ),
        (
            models.Device,
            {
                "device_type_uri": "device_type_name",
                "manufacturer_uri": "manufacturer_name",
                "status_uri": "status_uri",
            },
        ),
        (models.DeviceContactRole, {"role_uri": "role_name"}),
        (
            models.DeviceParameter,
            {
                "unit_uri": "unit_name",
            },
        ),
        (
            models.DeviceProperty,
            {
                "accuracy_unit_uri": "accuracy_unit_name",
                "aggregation_type_uri": "aggregation_type_name",
                "compartment_uri": "compartment_name",
                "property_uri": "property_name",
                "resolution_unit_uri": "resolution_unit_name",
                "sampling_media_uri": "sampling_media_name",
                "unit_uri": "unit_name",
            },
        ),
        (
            models.DeviceSoftwareUpdateAction,
            {
                "software_type_uri": "software_type_name",
            },
        ),
        (
            models.GenericConfigurationAction,
            {
                "action_type_uri": "action_type_name",
            },
        ),
        (
            models.GenericDeviceAction,
            {
                "action_type_uri": "action_type_name",
            },
        ),
        (
            models.GenericPlatformAction,
            {
                "action_type_uri": "action_type_name",
            },
        ),
        (
            models.Platform,
            {
                "manufacturer_uri": "manufacturer_name",
                "platform_type_uri": "platform_type_name",
                "status_uri": "status_name",
            },
        ),
        (models.PlatformContactRole, {"role_uri": "role_name"}),
        (
            models.PlatformParameter,
            {
                "unit_uri": "unit_name",
            },
        ),
        (
            models.PlatformSoftwareUpdateAction,
            {
                "software_type_uri": "software_type_name",
            },
        ),
        (
            models.Site,
            {
                "site_type_uri": "site_type_name",
                "site_usage_uri": "site_usage_uri",
            },
        ),
        (models.SiteContactRole, {"role_uri": "role_name"}),
    ]


@cv_group.command("apply-current-terms-to-sms")
@click.pass_context
def cv_apply_current_terms(ctx):
    """Query the CV and set the latest values in the SMS data models."""
    # This is the base url that points to the SMS CV - that the frontend can access.
    expected_cv_url_in_db = app.config["CV_URL"]
    # This is just a local setting so that we can overrite it url to a service internal
    # one in the local development setup.
    # If it is not set, then we just use the expected_cv_url_in_db - a url that we can
    # access on staging & production systems.
    cv_url_backend_access = os.environ.get(
        "CV_URL_BACKEND_ACCESS", expected_cv_url_in_db
    )

    cv_cache = {}

    for model_field, fields_to_update in ctx.obj["fields_to_check"]:
        for entry in db.session.query(model_field).all():
            for uri_field_name, name_field_name in fields_to_update.items():
                uri_value = getattr(entry, uri_field_name)
                name_value = getattr(entry, name_field_name)

                name_to_set = None
                if uri_value:
                    if uri_value in cv_cache.keys():
                        name_to_set = cv_cache[uri_value]
                    else:
                        if uri_value.startswith(expected_cv_url_in_db):
                            url = uri_value.replace(
                                expected_cv_url_in_db, cv_url_backend_access
                            )
                            response = requests.get(url)
                            if response.ok:
                                response_data = response.json()["data"]
                                term = response_data["attributes"]["term"]
                                name_to_set = term
                                cv_cache[uri_value] = name_to_set

                    if name_value != name_to_set and name_to_set is not None:
                        setattr(entry, name_field_name, name_to_set)

            db.session.add(entry)
    db.session.commit()


@cv_group.command("list-sms-entries-with-name-but-without-uri")
@click.pass_context
def cv_list_sms_entries_with_name_but_without_uri(ctx):
    """List all the sms entries with name values but without the according cv uris."""
    for model, fields_to_check in ctx.obj["fields_to_check"]:
        for entry in db.session.query(model).all():
            for uri_field_name, name_field_name in fields_to_check.items():
                uri_value = getattr(entry, uri_field_name)
                name_value = getattr(entry, name_field_name)

                if name_value and not uri_value:
                    print(
                        f"{model.__name__} {entry.id} {name_field_name}: '{name_value}'"
                    )


if __name__ == "__main__":
    cli()
