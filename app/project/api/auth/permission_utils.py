import click
from flask_jwt_extended import get_current_user
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    current_user,
    verify_jwt_in_request,
)
from sqlalchemy import or_, and_

from ..helpers.errors import ForbiddenError
from ..models.base_model import db
from ..services.idl_services import Idl


def is_user_in_a_group(groups_to_check):
    """
    Check if the current user is in the same group
    as the object regardless if it is admin or member.

    :param groups_to_check:
    :return:
    """
    if not groups_to_check:
        return True
    current_user = get_current_user()
    idl_groups = Idl().get_all_permission_groups(current_user.subject)
    user_groups = (
        idl_groups.administrated_permissions_groups
        + idl_groups.membered_permissions_groups
    )
    return any(group in user_groups for group in groups_to_check)


def is_user_admin_in_a_group(groups_to_check):
    """
    check if the current user is an admin in the same group
    as the object.

    :param groups_to_check: a list of ids
    :return:
    """
    if not groups_to_check:
        return True
    current_user = get_current_user()
    idl_groups = Idl().get_all_permission_groups(current_user.subject)
    user_groups = idl_groups.administrated_permissions_groups
    return any(group in user_groups for group in groups_to_check)


def is_superuser():
    """
    Check if current user is a super admin.

    :return: boolean
    """

    current_user = get_current_user()

    return current_user.is_superuser


def assert_current_user_is_owner_of_object(object_):
    """
    Checks if the current user is the owner of the given object.

    :param object_:
    :return:
    """
    current_user_id = get_current_user().id
    if current_user_id != object_.created_by_id:
        raise ForbiddenError(
            "This is a private object. You should be the owner to modify!"
        )


@jwt_required(optional=True)
def get_collection_with_permissions(model, collection, qs, view_kwargs):
    """Retrieve a collection of objects through sqlalchemy with permissions
    and take the intersection between them and requested collection.

    :param model:
    :param collection qs:
    :param dict view_kwargs: kwargs from the resource view
    :return set: list of objects
    """
    query = db.session.query(model)
    if get_jwt_identity() is None:
        query = query.filter_by(is_public=True)
    else:
        if not current_user.is_superuser:
            user_id = current_user.id
            query = query.filter(
                or_(
                    and_(model.is_private, model.created_by_id == user_id,),
                    or_(model.is_public, model.is_internal,),
                )
            )
    allowed_collection = query.all()

    return set(collection).intersection(allowed_collection)


def check_patch_permission(data, object_to_patch):
    """
    check if a user has the permission to patch an object.

    :param data:
    :param object_to_patch:
    """
    if not is_superuser():
        object_ = (
            db.session.query(object_to_patch).filter_by(id=data["id"]).one_or_none()
        )
        if object_.is_private:
            click.secho(object_.is_private, fg="green")
            assert_current_user_is_owner_of_object(object_)
        else:
            group_ids = object_.group_ids
            if not is_user_in_a_group(group_ids):
                raise ForbiddenError(
                    "User is not part of any group to edit this object."
                )


def check_deletion_permission(kwargs, object_to_delete):
    """
    check if a user has the permission to delete an object.

    :param kwargs:
    :param object_to_delete:
    """
    if not is_superuser():
        object_ = (
            db.session.query(object_to_delete).filter_by(id=kwargs["id"]).one_or_none()
        )
        group_ids = (
            db.session.query(object_to_delete)
            .filter_by(id=kwargs["id"])
            .one_or_none()
            .group_ids
        )
        if group_ids is None:
            assert_current_user_is_owner_of_object(object_)
        if not is_user_admin_in_a_group(group_ids):
            raise ForbiddenError("User is not part of any group to delete this object.")


def set_default_permission_view_to_internal_if_not_exists_or_all_false(data):
    """
    Check if the request doesn't include permission data (is_public, is_internal, is_private) or all are False
    and if not the set it to internal by default.

    :param data: json date sent wit the request.
    """
    if not any(
        [data.get("is_private"), data.get("is_public"), data.get("is_internal")]
    ):
        data["is_internal"] = True
        data["is_public"] = False
        data["is_private"] = False


def prevent_normal_user_from_viewing_not_owned_private_object(object_):
    """
    Check if user is not the owner of a private object and if so return a ForbiddenError.

    :param object_:
    """
    verify_jwt_in_request()
    user_id = current_user.id
    if not current_user.is_superuser:
        if object_.created_by_id != user_id:
            raise ForbiddenError("User is not allowed to view object.")


def check_for_permissions(model_class, kwargs):
    """
    check if a user has the permission to view an object.

    :param model_class: class model
    :param kwargs:
    """
    object_ = db.session.query(model_class).filter_by(id=kwargs["id"]).first()
    if object_:
        if object_.is_private:
            prevent_normal_user_from_viewing_not_owned_private_object(object_)
        elif object_.is_internal:
            verify_jwt_in_request()
