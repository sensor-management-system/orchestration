import datetime

from flask import current_app, g
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..helpers.db import save_to_db
from ..models import (
    ConfigurationAttachment,
    Contact,
    DeviceAttachment,
    PlatformAttachment,
    User,
    Device,
    Platform, Configuration,
)
from ..models.base_model import db
from ...api import minio


def add_contact_to_object(entity_with_contact_list):
    """
    Add created user to the object-contacts if it is not added in the data
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


def delete_attachments_in_minio_by_url(url):
    """
    Use the minio class to delete an attachment.

    :param url: attachment url.
    """
    still_in_use = False
    for model in [DeviceAttachment, PlatformAttachment, ConfigurationAttachment]:
        possible_entry = db.session.query(model).filter_by(url=url).first()
        if possible_entry:
            still_in_use = True
            break

    if not still_in_use:
        minio.remove_an_object(url)


def delete_attachments_in_minio_by_related_object_id(
    related_object_class, attachment_class, object_id_intended_for_deletion
):
    """
    Delete an Attachment related to an object by Using the minio class
     to delete it or a list of attachments.
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


def set_update_description_text_and_update_by_user(obj_, msg):
    obj_.update_description = msg
    obj_.updated_by_id = g.user.id
    save_to_db(obj_)


def query_device_and_set_update_description_text(msg, result_id):
    """
    Get the device and add update_description text to it.

    :param msg: a text of what did change.
    :param result_id: the id of the object
    """
    device = db.session.query(Device).filter_by(id=result_id).first()
    set_update_description_text_and_update_by_user(device, msg)


def query_platform_and_set_update_description_text(msg, result_id):
    """
    Get the platform and add update_description text to it.

    :param msg: a text of what did change.
    :param result_id: the id of the object
    """
    platform = db.session.query(Platform).filter_by(id=result_id).first()
    set_update_description_text_and_update_by_user(platform, msg)


def query_configuration_and_set_update_description_text(msg, result_id):
    """
    Get the configuration and add update_description text to it.

    :param msg: a text of what did change.
    :param result_id: the id of the object
    """
    configuration = db.session.query(Configuration).filter_by(id=result_id).first()
    set_update_description_text_and_update_by_user(configuration, msg)


def add_pid(obj_, pid_string):
    """
    Add PID to an existed object.

    :param obj_: the existed object.
    :param pid_string: pid of the entity.
    """
    obj_.persistent_identifier = pid_string
    # Set the datetime and user how did ask to
    # add a pid to the entity
    obj_.updated_at = datetime.datetime.utcnow()
    obj_.updated_by = g.user

    db.session.add(obj_)
    db.session.commit()
