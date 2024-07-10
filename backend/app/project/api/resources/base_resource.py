# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Some methods to use in various resource classes."""

from flask import g
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ...api import minio
from ...extensions.instances import pidinst
from ..helpers.db import save_to_db
from ..models import (
    ActivityLog,
    Configuration,
    ConfigurationAttachment,
    Contact,
    Device,
    DeviceAttachment,
    Platform,
    PlatformAttachment,
    Site,
    User,
)
from ..models.base_model import db


def add_contact_to_object(entity_with_contact_list):
    """
    Add created user to the object-contacts.

    :param entity_with_contact_list:
    :return:
    """
    user_entry = (
        db.session.query(User)
        .filter_by(id=entity_with_contact_list.created_by_id)
        .first()
    )
    contact_id = user_entry.contact_id
    contact_entry = db.session.query(Contact).filter_by(id=contact_id).first()
    contacts = entity_with_contact_list.contacts
    if contact_entry not in contacts:
        contacts.append(contact_entry)
        db.session.add(entity_with_contact_list)
        db.session.commit()
    return contact_entry


def delete_attachments_in_minio_by_url(internal_url):
    """
    Use the minio class to delete an attachment.

    :param url: attachment url.
    """
    still_in_use = False
    if internal_url:
        for model in [DeviceAttachment, PlatformAttachment, ConfigurationAttachment]:
            possible_entry = (
                db.session.query(model).filter_by(internal_url=internal_url).first()
            )
            if possible_entry:
                still_in_use = True
                break

    if not still_in_use:
        minio.remove_an_object(internal_url)


def delete_attachments_in_minio_by_related_object_id(
    related_object_class, attachment_class, object_id_intended_for_deletion
):
    """
    Delete an Attachment related to an object.

    Uses the minio class.

    :param object_id_intended_for_deletion:  object id.
    :param related_object_class: class od object the Attachment related to.
    :param attachment_class: attachment class.
    """
    related_object = (
        db.session.query(related_object_class)
        .filter_by(id=object_id_intended_for_deletion)
        .first()
    )
    attachment = (
        db.session.query(attachment_class)
        .filter_by(id=related_object.attachment_id)
        .first()
    )
    minio.remove_an_object(attachment.url)


def check_if_object_not_found(model_class, kwargs):
    """
    Check if an object is none and raise a 404.

    :param model_class:
    :param kwargs:
    :return:
    """
    object_to_be_checked = (
        db.session.query(model_class).filter_by(id=kwargs["id"]).first()
    )
    if object_to_be_checked is None:
        raise ObjectNotFound({"pointer": ""}, "Object Not Found")
    else:
        return object_to_be_checked


def set_update_description_text_user_and_pidinst(obj_, msg):
    """
    Set the update description & user and save it to the db.

    Also update the metadata in case we have a pidinst record
    on the entry.
    """
    obj_.update_description = msg
    obj_.updated_by_id = g.user.id
    save_to_db(obj_)
    new_log_entry = ActivityLog.create(
        entity=obj_,
        user=g.user,
        description=msg,
    )
    save_to_db(new_log_entry)

    if pidinst.has_external_metadata(obj_):
        pidinst.update_external_metadata(obj_)


def query_device_set_update_description_and_update_pidinst(msg, result_id):
    """
    Get the device and add update_description text to it.

    :param msg: a text of what did change.
    :param result_id: the id of the object
    """
    device = db.session.query(Device).filter_by(id=result_id).first()
    set_update_description_text_user_and_pidinst(device, msg)


def query_platform_set_update_description_and_update_pidinst(msg, result_id):
    """
    Get the platform and add update_description text to it.

    :param msg: a text of what did change.
    :param result_id: the id of the object
    """
    platform = db.session.query(Platform).filter_by(id=result_id).first()
    set_update_description_text_user_and_pidinst(platform, msg)


def query_configuration_set_update_description_and_update_pidinst(msg, result_id):
    """
    Get the configuration and set the update_description text.

    :param msg: a text of what did change.
    :param result_id: the id of the object
    """
    configuration = db.session.query(Configuration).filter_by(id=result_id).first()
    set_update_description_text_user_and_pidinst(configuration, msg)


def query_site_set_update_description_and_update_pidinst(msg, result_id):
    """Get the configuration and add update description text."""
    # Honestly we don't have pidinst support for the sites yet.
    site = db.session.query(Site).filter_by(id=result_id).first()
    set_update_description_text_user_and_pidinst(site, msg)
