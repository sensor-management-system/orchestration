from ..auth.flask_openidconnect import open_id_connect
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..models import (
    ConfigurationAttachment,
    Contact,
    DeviceAttachment,
    PlatformAttachment, User,
)
from ..models.base_model import db
from ...api import minio


def add_created_by_id(data):
    """
    Use jwt to add user id to dataset.
    :param data:
    :param args:
    :param kwargs:
    :return:

    .. note:: every HTTP-Methode should come with a json web token, which automatically
    check if the user exists or add the user to the database
    so that a user can't be None. Due to that created_by_id can't be None also.
    """
    user_entry = open_id_connect.get_current_user()
    data["created_by_id"] = user_entry.id


def add_updated_by_id(data):
    """
    Use jwt to add user id to dataset after updating the data.
    :param data:
    :param args:
    :param kwargs:
    :return:

    """
    user_entry = open_id_connect.get_current_user()
    data["updated_by_id"] = user_entry.id


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
