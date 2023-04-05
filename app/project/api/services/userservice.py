# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from ..models import Device, Platform, Configuration
from ..models.contact import device_contacts, platform_contacts, configuration_contacts
from ... import db


def user_deactivation(src_user, src_contact, dest_contact):
    """
    Deactivate a user in this steps:
     - Set the active attribute to False
     - Replace contact entities with a deactivation message.

    :param src_user: user object Intended to be deactivated.
    :param src_contact: substituted user object.
    :param dest_contact: contact-object for the substituted user.
    """

    # deactivate the user account
    src_user.active = False
    # deactivate the it contact account
    src_contact.active = False
    # replace the user data with a message contains only
    # user id.
    remove_contact_data(src_contact, src_user)

    # Search for all dependencies connected to a contact.
    # At the main time we don't replace anything but we could.
    search_and_replace_referencing_foreign_keys(src_contact, dest_contact, src_user)

    db.session.commit()


def add_substituted_user(table, object_, object_id, dest_contact):
    """
    Add an Other user to the associated table.

    :param table: associated table.
    :param object_: Object class.
    :param object_id: object id field name
    :param dest_contact: destination contact-object

    """
    for object_in_table in table:
        # Converting a query result to dict
        object_as_dict = object_in_table._asdict()
        o = db.session.query(object_).filter_by(id=object_as_dict[object_id]).first()
        o.contacts.append(dest_contact)


def search_database_tables_and_add_substituted_user(dest_contact, src_user):
    """
    Add substituted user whenever the source user was listed in the associated tables.

    :param dest_contact: destination contact-object
    :param src_user: source user_object
    :return:
    """

    device_contact_table = (
        db.session.query(device_contacts)
        .filter_by(contact_id=src_user.contact_id)
        .all()
    )
    add_substituted_user(device_contact_table, Device, "device_id", dest_contact)

    platform_contact_table = (
        db.session.query(platform_contacts)
        .filter_by(contact_id=src_user.contact_id)
        .all()
    )
    add_substituted_user(platform_contact_table, Platform, "platform_id", dest_contact)

    configuration_contact_table = (
        db.session.query(configuration_contacts)
        .filter_by(contact_id=src_user.contact_id)
        .all()
    )
    add_substituted_user(
        configuration_contact_table, Configuration, "configuration_id", dest_contact
    )


def search_and_replace_referencing_foreign_keys(src_contact, dest_contact, src_user):
    """
    Search and replace referencing foreign keys in booth classes and associated tables.

    :param src_contact: source contact-object
    :param dest_contact: destination contact-object
    :param src_user: source user_object
    :return:
    """

    # search the Many-to-Many tables as they have no Classes
    if dest_contact is not None:
        search_database_tables_and_add_substituted_user(dest_contact, src_user)


def remove_contact_data(src_contact, src_user):
    """
    Replace the user data with a message contains only
    user id.

    :param src_contact: contact object.
    :param src_user: user object.

    """
    message = f"User {src_user.id} is deactivated"
    src_contact.given_name = message
    src_contact.family_name = message
    src_contact.email = message
    src_contact.website = message
    src_contact.orcid = None
    src_contact.organization = message
