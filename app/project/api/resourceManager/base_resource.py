import click
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user, verify_jwt_in_request
from sqlalchemy import and_, or_

from ..helpers.errors import ForbiddenError
from ..helpers.permission import is_user_super_admin, assert_current_user_is_owner_of_object, is_user_in_a_group, \
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
            assert_current_user_is_owner_of_object(object_)
        else:
            group_ids = object_.group_ids
            if is_user_in_a_group(group_ids):
                add_updated_by_id(data)
            else:
                raise ForbiddenError("User is not part of any group to edit this object.")


def check_deletion_permission(kwargs, object_to_delete):
    """

    :param kwargs:
    :param object_to_delete:
    :return:
    """
    if not is_user_super_admin():
        group_ids = db.session.query(object_to_delete).filter_by(id=kwargs['id']).one_or_none().group_ids
        if not is_user_admin_in_a_group(group_ids):
            raise ForbiddenError("User is not part of any group to edit this object.")


@jwt_required(optional=True)
def set_permission_filter_to_query(model_class):
    """
    This methode do the choices:
    - if user is anonymous then show only public objects.
    - if the user is superuser the show all.
    - if user logged in then show public, internal and owned private objects.

    :param model_class:
    :return:
    """
    query_ = model_class.query

    if get_jwt_identity() is None:
        query_ = query_.filter_by(is_public=True)
    else:
        if not current_user.is_superuser:
            user_id = current_user.id
            query_ = query_.filter(
                or_(
                    and_(
                        model_class.is_private,
                        model_class.created_by_id == user_id
                    ),
                    or_(
                        model_class.is_public,
                        model_class.is_internal
                    )
                )
            )
    return query_


def set_default_permission_view_to_internal_if_not_exists_or_all_false(data):
    """
    Methode to check if the request doesn't include the permission view or all are False
    and if not the set it to internal by default.

    :param data: json date sent wit the request.
    """
    if not any([bool(data.get("is_private")), bool(data.get("is_public")), bool(data.get("is_internal"))]):
        data["is_internal"] = True
        data["is_public"] = False
        data["is_private"] = False


def prevent_normal_user_from_viewing_not_owned_private_object(model_class, kwargs):
    """
    checks if user is not the owner of a private object and if so return a ForbiddenError.

    :param kwargs:
    :param model_class: class model
    :return:
    """
    object_ = db.session.query(model_class).filter_by(id=kwargs["id"]).first()
    if object_.is_private:
        verify_jwt_in_request()
        user_id = current_user.id
        if not current_user.is_superuser:
            if object_.created_by_id != user_id:
                raise ForbiddenError("User is not allowed to view object.")
    elif object_.is_internal:
        verify_jwt_in_request()
