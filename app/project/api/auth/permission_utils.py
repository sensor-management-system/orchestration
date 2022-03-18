"""Utility functions to handle permissions."""

import json
from json import JSONDecodeError

from flask import request
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy import and_, or_

from ..auth.flask_openidconnect import open_id_connect
from ..datalayers.esalchemy import AndFilter, OrFilter, TermEqualsExactStringFilter
from ..helpers.errors import ForbiddenError, BadRequestError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Configuration
from ..models import Device, Platform
from ..models.base_model import db
from ..services.idl_services import Idl
from ..token_checker import current_user_or_none


def is_user_in_a_group(groups_to_check):
    """
    Check if the current user is in the same group as the object.

    Doesn't care if the user is an admin or a member.

    :param groups_to_check:
    :return: boolean
    """
    if not groups_to_check:
        return True
    current_user = open_id_connect.get_current_user()
    idl_groups = Idl().get_all_permission_groups_for_a_user(current_user.subject)
    if not idl_groups:
        return []
    user_groups = (
        idl_groups.administrated_permission_groups
        + idl_groups.membered_permission_groups
    )
    return any(group in user_groups for group in groups_to_check)


def is_user_admin_in_a_group(groups_to_check):
    """
    Check if the current user is an admin in the same group as the object.

    :param groups_to_check: a list of ids
    :return: boolean
    """
    if not groups_to_check:
        return True
    current_user = open_id_connect.get_current_user()
    idl_groups = Idl().get_all_permission_groups_for_a_user(current_user.subject)
    if not idl_groups:
        return []
    user_groups = idl_groups.administrated_permission_groups
    return any(group in user_groups for group in groups_to_check)


def is_superuser():
    """
    Check if current user is a super admin.

    :return: boolean
    """
    current_user = open_id_connect.get_current_user()

    return current_user.is_superuser


def assert_current_user_is_owner_of_object(object_):
    """
    Check if the current user is the owner of the given object.

    Raises an ForbiddenError in case the user is not owner of the object.

    :param object_:
    :return: None
    """
    current_user_id = open_id_connect.get_current_user().id
    if current_user_id != object_.created_by_id:
        raise ForbiddenError(
            "This is a private object. You should be the owner to modify!"
        )


def get_query_with_permissions(model):
    """
    Filter a model query for those data that the user is allowed to see.

    :param model:
    :return set: queryset for the model
    """
    query = db.session.query(model)
    current_user = current_user_or_none(optional=True)
    if current_user is None:
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
    return query


def get_es_query_with_permissions():
    """
    Filter a model query for those data that the user is allowed to see.

    :return set: queryset for the model
    """
    current_user = current_user_or_none(optional=True)
    if current_user is None:
        return TermEqualsExactStringFilter("is_public", True)
    if not current_user.is_superuser:
        user_id = current_user.id
        return OrFilter(
            [
                AndFilter(
                    [
                        TermEqualsExactStringFilter("is_private", True),
                        TermEqualsExactStringFilter("created_by_id", user_id),
                    ]
                ),
                OrFilter(
                    [
                        TermEqualsExactStringFilter("is_public", True),
                        TermEqualsExactStringFilter("is_internal", True),
                    ]
                ),
            ]
        )
    return None


def check_patch_permission(data, object_to_patch):
    """
    Check if a user has the permission to patch an object.

    :param data:
    :param object_to_patch:
    """
    if not is_superuser():
        object_ = (
            db.session.query(object_to_patch).filter_by(id=data["id"]).one_or_none()
        )
        if object_:
            if object_.is_private:
                assert_current_user_is_owner_of_object(object_)
            else:
                group_ids = object_.group_ids
                if not is_user_in_a_group(group_ids):
                    raise ForbiddenError(
                        "User is not part of any group to edit this object."
                    )
                allow_only_admin_in_a_permission_group_to_remove_it_from_an_object(
                    group_ids
                )
        else:
            raise ObjectNotFound(f"Object with id: {data['id']} not found!")

    # Add update by id to data
    add_updated_by_id(data)


def check_deletion_permission(kwargs, object_to_delete):
    """
    Check if a user has the permission to delete an object.

    :param kwargs:
    :param object_to_delete:
    """
    if not is_superuser():
        object_ = (
            db.session.query(object_to_delete).filter_by(id=kwargs["id"]).one_or_none()
        )
        if object_to_delete == Configuration:
            group_id = (
                db.session.query(object_to_delete)
                .filter_by(id=kwargs["id"])
                .one_or_none()
                .cfg_permission_group
            )
            group_ids = [group_id] if group_id else []
        else:
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
    Check if the request doesn't include permission data or all are False.

    Checks are for is_public, is_internal or is_private.
    If none of them are true, we set internal as default.
    and if not the set it to internal by default.

    :param data: json date sent wit the request.
    """
    if not any(
        [data.get("is_private"), data.get("is_public"), data.get("is_internal")]
    ):
        data["is_internal"] = True
        data["is_public"] = False
        data["is_private"] = False

    # Add created by id to data
    add_created_by_id(data)


def prevent_normal_user_from_viewing_not_owned_private_object(object_):
    """
    Check if user is not the owner of a private object and if so return a ForbiddenError.

    :param object_:
    """
    current_user = current_user_or_none()
    user_id = current_user.id
    if not current_user.is_superuser:
        if object_.created_by_id != user_id:
            raise ForbiddenError("User is not allowed to view object.")


def check_for_permissions(model_class, kwargs):
    """
    Check if a user has the permission to view an object.

    :param model_class: class model
    :param kwargs:
    """
    object_ = db.session.query(model_class).filter_by(id=kwargs["id"]).first()
    if object_:
        if object_.is_private:
            prevent_normal_user_from_viewing_not_owned_private_object(object_)
        elif object_.is_internal:
            current_user_or_none()
    else:
        raise ObjectNotFound({"pointer": ""}, "Object Not Found")


def allow_only_admin_in_a_permission_group_to_remove_it_from_an_object(group_ids):
    """
    Ensure that a remove of a permission group can only be done by an admin.

    Only admins in a permission groups are allowed to perform a remove action
    fron the permission group list.
    This methode will be applied before a patch request for (device, platform).

    :param group_ids: list of the permission groups_ids from database.
    """
    # An example how the json_data:
    # {
    #   "data": {
    #     "type": "device",
    #     "id": 2,
    #     "attributes": {
    #       "short_name": "internal Device with a group 6",
    #       "is_public": false,
    #       "is_private": false,
    #       "is_internal": true,
    #       "group_ids": [
    #         6
    #       ]
    #     }
    #   }
    # }
    json_data = request.get_json() or {}
    if "group_ids" in json_data["data"]["attributes"]:
        changed_group = json_data["data"]["attributes"]["group_ids"]
        if group_ids != changed_group:
            # Get permission groups_ids deleted from the original permission groups
            deleted_elements = list(set(group_ids) - set(changed_group))
            if deleted_elements:
                for element in deleted_elements:
                    if not is_user_admin_in_a_group([element]):
                        raise ForbiddenError("Not allowed to perform this action.")


def check_permissions_for_related_objects(model_class, id_):
    """
    check if a user has the permission to view a related object by checking
    the object permission.

    :param id_:
    :param model_class: class model
    """
    object_ = db.session.query(model_class).filter_by(id=id_).first()
    if object_ is None:
        raise ObjectNotFound("Object not found!")
    related_object = object_.get_parent()
    if related_object.is_private:
        assert_current_user_is_owner_of_object(related_object)
    elif not related_object.is_public:
        current_user_or_none()


def check_post_permission_for_related_objects():
    """
    check if a user has the permission to patch a related object.
    """
    try:
        data = json.loads(request.data.decode())["data"]
    except JSONDecodeError as e:
        raise BadRequestError(repr(e))
    related_object = None
    if not is_superuser():
        if "device" in data["relationships"]:
            object_id = data["relationships"]["device"]["data"]["id"]
            related_object = (
                db.session.query(Device).filter_by(id=object_id).one_or_none()
            )
        if "platform" in data["relationships"]:
            object_id = data["relationships"]["platform"]["data"]["id"]
            related_object = (
                db.session.query(Platform).filter_by(id=object_id).one_or_none()
            )
        if related_object is not None:
            if related_object.is_private:
                assert_current_user_is_owner_of_object(related_object)
            else:
                group_ids = related_object.group_ids
                if not is_user_in_a_group(group_ids):
                    raise ForbiddenError(
                        "User is not part of any group to edit this object."
                    )
        else:
            raise ObjectNotFound("Object not found!")


def check_patch_permission_for_related_objects(data, object_to_patch):
    """
    check if a user has the permission to patch a related object.

    :param data:
    :param object_to_patch:
    """
    if not is_superuser():
        object_ = (
            db.session.query(object_to_patch).filter_by(id=data["id"]).one_or_none()
        )
        if object_ is None:
            raise ObjectNotFound("Object not found!")
        related_object = object_.get_parent()
        if related_object.is_private:
            assert_current_user_is_owner_of_object(related_object)
        else:
            group_ids = related_object.group_ids
            if not is_user_in_a_group(group_ids):
                raise ForbiddenError(
                    "User is not part of any group to edit this object."
                )


def check_deletion_permission_for_related_objects(kwargs, object_to_delete):
    """
    check if a user has the permission to delete a related object.

    :param kwargs:
    :param object_to_delete:
    """
    if not is_superuser():
        object_ = (
            db.session.query(object_to_delete).filter_by(id=kwargs["id"]).one_or_none()
        )
        if object_ is None:
            raise ObjectNotFound("Object not found!")
        related_object = object_.get_parent()
        group_ids = related_object.group_ids
        if group_ids is None:
            assert_current_user_is_owner_of_object(related_object)
        if not is_user_admin_in_a_group(group_ids):
            raise ForbiddenError("User is not part of any group to delete this object.")


def get_query_with_permissions_for_related_objects(model):
    """Retrieve a collection of related objects through sqlalchemy by checking
    the object permission.

    :param model:
    :return set: list of objects
    """
    query = db.session.query(model)
    current_user = current_user_or_none(optional=True)
    if hasattr(model, "device"):
        related_object = model.device
    else:
        related_object = model.platform
    if current_user is None:
        query = query.filter(related_object.has(is_public=True))
    else:
        if not current_user.is_superuser:
            query = query.filter(
                or_(
                    related_object.has(is_public=True),
                    related_object.has(is_internal=True),
                    and_(
                        related_object.has(is_private=True),
                        related_object.has(created_by_id=current_user.id),
                    ),
                )
            )

    return query
