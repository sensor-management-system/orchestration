from flask_jwt_extended import get_jwt_identity

from ..models import Contact, User
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
    current_user = get_jwt_identity()
    user_entry = db.session.query(User).filter_by(subject=current_user).first()
    data["created_by_id"] = user_entry.id


def add_updated_by_id(data):
    """
    Use jwt to add user id to dataset after updating the data.
    :param data:
    :param args:
    :param kwargs:
    :return:

    """
    current_user = get_jwt_identity()
    user_entry = db.session.query(User).filter_by(subject=current_user).first()
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


def delete_attachments_in_minio_by_id(_class, object_id_intended_for_deletion):
    """
    Use the minio class to delete an attachment or a list of attachments.
    :param object_id_intended_for_deletion:
    :param _class:
    :return:
    """
    attachment = (
        db.session.query(_class)
            .filter_by(id=object_id_intended_for_deletion)
            .first()
    )
    minio.remove_an_object(attachment.url)
