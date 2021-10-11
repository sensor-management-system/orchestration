import click
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user
from sqlalchemy import and_, or_

from ..helpers.errors import ForbiddenError
from ..helpers.permission import is_user_super_admin, is_user_owner_of_this_object, is_user_in_a_group, \
    is_user_admin_in_a_group
from ..models import (
    ConfigurationAttachment,
    Contact,
    DeviceAttachment,
    PlatformAttachment,
    User,
)
from ..models.base_model import db
from ...api import minio


def add_created_by_id(data):
    """
    Use jwt to add user id to dataset.
    :param data:
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


def check_patch_permission(data, object_to_patch):
    """

    :param data:
    :param object_to_patch:
    :return:
    """
    if not is_user_super_admin():
        object_ = db.session.query(object_to_patch).filter_by(id=data['id']).one_or_none()
        if object_.is_private:
            click.secho(object_.is_private, fg="green")
            is_user_owner_of_this_object(object_)
        else:
            groups_ids = object_.groups_ids
            if is_user_in_a_group(groups_ids):
                add_updated_by_id(data)
            else:
                raise ForbiddenError(f"User should be in this groups: {groups_ids}")


def check_deletion_permission(kwargs, object_to_patch):
    """

    :param kwargs:
    :param object_to_patch:
    :return:
    """
    if not is_user_super_admin():
        groups_ids = db.session.query(object_to_patch).filter_by(id=kwargs['id']).one_or_none().groups_ids
        if not is_user_admin_in_a_group(groups_ids):
            raise ForbiddenError(f"User should be admin in one of this groups: {groups_ids}")


@jwt_required(optional=True)
def set_object_query(object_):
    """
    This methode do the choices:
    - if user is anonymous then show only public objects.
    - if the user is superuser the show all.
    - if user logged in then show public, internal and owned private objects.

    :param object_:
    :return:
    """
    query_ = object_.query

    if get_jwt_identity() is None:
        query_ = query_.filter_by(is_public=True)
    else:
        if not current_user.is_superuser:
            user_id = current_user.id
            query0 = object_.query
            query0 = query0.filter(
                and_(
                    object_.is_private,
                    object_.created_by_id == user_id
                )
            )
            query_ = query_.filter(
                or_(
                    object_.is_public,
                    object_.is_internal
                )
            )

            query_ = query_.union(query0)
    return query_
