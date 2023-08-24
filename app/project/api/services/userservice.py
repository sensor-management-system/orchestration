# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Functions to run the actions on user objects."""

from ... import db
from ...extensions.instances import pidinst
from ..models import (
    ConfigurationContactRole,
    DeviceContactRole,
    PlatformContactRole,
    SiteContactRole,
)


def user_deactivation(src_user, src_contact, dest_contact):
    """
    Deactivate a user.

    This includes the following steps:
     - Set the active attribute to False
     - Replace contact entities with a deactivation message.
     - update external metadata (pidinst).

    :param src_user: user object Intended to be deactivated.
    :param src_contact: substituted user object.
    :param dest_contact: contact-object for the substituted user.
    """
    # Deactivate the user account
    src_user.active = False
    # Deactivate its contact
    src_contact.active = False
    # Replace the user data with a message contains only user id.
    overwrite_contact_data(src_contact, src_user)

    # Search for all dependencies connected to a contact.
    # Replace it with the dest_contact in case we got one.
    associated_objects = search_and_replace_referencing_foreign_keys(
        src_contact, dest_contact, src_user
    )

    db.session.commit()

    # And update external metadata that are handled on the device, platform
    # or configuration level.
    for entry in associated_objects:
        if pidinst.has_external_metadata(entry):
            # We don't run async in order to make sure that we run all the requests
            # and don't stop the cli script before the other threads run.
            pidinst.update_external_metadata(entry, run_async=False)


def search_and_replace_referencing_foreign_keys(src_contact, dest_contact, src_user):
    """
    Search and replace referencing foreign keys in booth classes and associated tables.

    :param src_contact: source contact-object
    :param dest_contact: destination contact-object
    :param src_user: source user_object
    :return: set of associated objects
    """
    associated_objects = set()

    device_contact_roles = (
        db.session.query(DeviceContactRole)
        .filter_by(contact_id=src_user.contact_id)
        .all()
    )
    platform_contact_roles = (
        db.session.query(PlatformContactRole)
        .filter_by(contact_id=src_user.contact_id)
        .all()
    )
    configuration_contact_roles = (
        db.session.query(ConfigurationContactRole)
        .filter_by(contact_id=src_user.contact_id)
        .all()
    )
    site_contact_roles = (
        db.session.query(SiteContactRole)
        .filter_by(contact_id=src_user.contact_id)
        .all()
    )

    for role in device_contact_roles:
        associated_objects.add(role.device)
    for role in platform_contact_roles:
        associated_objects.add(role.platform)
    for role in configuration_contact_roles:
        associated_objects.add(role.configuration)
    for role in site_contact_roles:
        associated_objects.add(role.site)

    if dest_contact is not None:
        for role in device_contact_roles:
            if (
                db.session.query(DeviceContactRole)
                .filter_by(
                    contact_id=dest_contact.id,
                    device_id=role.device_id,
                    role_name=role.role_name,
                    role_uri=role.role_uri,
                )
                .first()
            ):
                db.session.delete(role)
            else:
                role.contact = dest_contact
                db.session.add(role)

        for role in platform_contact_roles:
            if (
                db.session.query(PlatformContactRole)
                .filter_by(
                    contact_id=dest_contact.id,
                    platform_id=role.platform_id,
                    role_name=role.role_name,
                    role_uri=role.role_uri,
                )
                .first()
            ):
                db.session.delete(role)
            else:
                role.contact = dest_contact
                db.session.add(role)

        for role in configuration_contact_roles:
            if (
                db.session.query(ConfigurationContactRole)
                .filter_by(
                    contact_id=dest_contact.id,
                    configuration_id=role.configuration_id,
                    role_name=role.role_name,
                    role_uri=role.role_uri,
                )
                .first()
            ):
                db.session.delete(role)
            else:
                role.contact = dest_contact
                db.session.add(role)

        for role in site_contact_roles:
            if (
                db.session.query(SiteContactRole)
                .filter_by(
                    contact_id=dest_contact.id,
                    site_id=role.site_id,
                    role_name=role.role_name,
                    role_uri=role.role_uri,
                )
                .first()
            ):
                db.session.delete(role)
            else:
                role.contact = dest_contact
                db.session.add(role)

    return associated_objects


def overwrite_contact_data(src_contact, src_user):
    """
    Replace the user data with a message contains only the user id.

    :param src_contact: contact object.
    :param src_user: user object.
    """
    message = f"User {src_user.id} is deactivated"
    src_contact.given_name = message
    src_contact.family_name = message
    src_contact.email = message
    src_contact.website = ""
    src_contact.orcid = None
    src_contact.organization = ""
