import json

from flask import request
from flask_jwt_extended import get_current_user
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    current_user,
    verify_jwt_in_request,
)
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy import or_, and_

from ..helpers.errors import ForbiddenError
from ..models import Configuration, Device, Platform
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
    check if the current user is an admin in the same group
    as the object.

    :param groups_to_check: a list of ids
    :return:
    """
    if not groups_to_check:
        return True
    current_user = get_current_user()
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
    else:
        raise ObjectNotFound({"pointer": ""}, "Object Not Found")


def allow_only_admin_in_a_permission_group_to_remove_it_from_an_object(group_ids):
    """
    Only admin in a permission groups is allowed to perform a remove action fron the permission group list.
    This Methode will be applied before a patch request for (device, platform)

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
    if hasattr(object_, "device"):
        if not object_.device.is_public:
            verify_jwt_in_request()
    elif hasattr(object_, "platform"):
        if not object_.platform.is_public:
            verify_jwt_in_request()


def check_post_permission_for_related_objects(object_):
    """
    check if a user has the permission to patch a related object.

    :param object_:
    """
    data = json.loads(request.data.decode())["data"]
    if not is_superuser():
        if "device" in data["relationships"]:
            object_id = data["relationships"]["device"]["data"]["id"]
            object_ = db.session.query(Device).filter_by(id=object_id).one_or_none()

        if "platform" in data["relationships"]:
            object_id = data["relationships"]["platform"]["data"]["id"]
            object_ = db.session.query(Platform).filter_by(id=object_id).one_or_none()

        if object_.is_private:
            assert_current_user_is_owner_of_object(object_)
        else:
            group_ids = object_.group_ids
            if not is_user_in_a_group(group_ids):
                raise ForbiddenError(
                    "User is not part of any group to edit this object."
                )


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
        if hasattr(object_, "device"):
            related_object = object_.device
        else:
            related_object = object_.platform
        if related_object.is_private:
            assert_current_user_is_owner_of_object(object_)
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
        if hasattr(object_, "device"):
            related_object = object_.device
        else:
            related_object = object_.platform
        group_ids = related_object.group_ids
        if group_ids is None:
            assert_current_user_is_owner_of_object(object_)
        if not is_user_admin_in_a_group(group_ids):
            raise ForbiddenError("User is not part of any group to delete this object.")


@jwt_required(optional=True)
def get_collection_with_permissions_for_related_objects(model, collection):
    """Retrieve a collection of related objects through sqlalchemy by checking
    the object permission.

    :param model:
    :param collection:
    :return set: list of objects
    """
    query = db.session.query(model)
    if get_jwt_identity() is None:
        if hasattr(model, "device"):
            query = query.filter(model.device.has(is_public=True))
        else:
            query = query.filter(model.platform.has(is_public=True))
    else:
        if not current_user.is_superuser:
            if hasattr(model, "device"):
                query = query.filter(
                    or_(
                        model.device.has(is_public=True),
                        model.device.has(is_internal=True),
                    )
                )
            else:
                query = query.filter(
                    or_(
                        model.platform.has(is_public=True),
                        model.platform.has(is_internal=True),
                    )
                )
    allowed_collection = query.all()

    return set(collection).intersection(allowed_collection)
