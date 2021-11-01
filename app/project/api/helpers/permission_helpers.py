from operator import and_

import click
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    current_user,
    verify_jwt_in_request,
)
from sqlalchemy import or_

from .errors import ForbiddenError
from .permission import (
    is_superuser,
    assert_current_user_is_owner_of_object,
    is_user_in_a_group,
    is_user_admin_in_a_group,
)
from ... import db


@jwt_required(optional=True)
def get_collection_with_permissions(cls, filters, qs, view_kwargs):
    """Retrieve a collection of objects through sqlalchemy with permissions

    :param cls:
    :param QueryStringManager qs: a querystring manager to retrieve information from url
    :param dict view_kwargs: kwargs from the resource view
    :param dict filters: A dictionary of key/value filters to apply to the eventual query
    :return tuple: the number of object and the list of objects
    """

    cls._data_layer.before_get_collection(qs, view_kwargs)
    query = cls._data_layer.query(view_kwargs)
    if get_jwt_identity() is None:
        query = query.filter_by(is_public=True)
    else:
        if not current_user.is_superuser:
            user_id = current_user.id
            query = query.filter(
                or_(
                    and_(
                        cls._data_layer.model.is_private,
                        cls._data_layer.model.created_by_id == user_id,
                    ),
                    or_(
                        cls._data_layer.model.is_public,
                        cls._data_layer.model.is_internal,
                    ),
                )
            )
    if filters:
        query = query.filter_by(**filters)
    if qs.filters:
        query = cls._data_layer.filter_query(query, qs.filters, cls._data_layer.model)
    if qs.sorting:
        query = cls._data_layer.sort_query(query, qs.sorting)
    object_count = query.count()
    if getattr(cls, "eagerload_includes", True):
        query = cls._data_layer.eagerload_includes(query, qs)
    query = cls._data_layer.paginate_query(query, qs.pagination)
    collection = query.all()
    collection = cls._data_layer.after_get_collection(collection, qs, view_kwargs)
    return object_count, collection


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
        group_ids = (
            db.session.query(object_to_delete)
            .filter_by(id=kwargs["id"])
            .one_or_none()
            .group_ids
        )
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
