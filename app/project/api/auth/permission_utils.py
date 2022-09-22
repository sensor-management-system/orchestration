"""Utility functions to handle permissions."""

from flask import g, request
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy import and_, or_

from ...extensions.instances import idl
from ..datalayers.esalchemy import AndFilter, OrFilter, TermEqualsExactStringFilter
from ..helpers.errors import ConflictError, ForbiddenError, UnauthorizedError
from ..helpers.resource_mixin import add_created_by_id, decode_json_request_data
from ..models import Configuration, Device, Platform
from ..models.base_model import db


def is_user_in_a_group(groups_to_check):
    """
    Check if the current user is in the same group as the object.

    Doesn't care if the user is an admin or a member.

    :param groups_to_check:
    :return: boolean
    """
    if not groups_to_check:
        return True
    idl_groups = idl.get_all_permission_groups_for_a_user(g.user.subject)
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
    idl_groups = idl.get_all_permission_groups_for_a_user(g.user.subject)
    if not idl_groups:
        return []
    user_groups = idl_groups.administrated_permission_groups
    return any(group in user_groups for group in groups_to_check)


def is_superuser():
    """
    Check if current user is a super admin.

    :return: boolean
    """
    return g.user and g.user.is_superuser


def assert_current_user_is_superuser_or_owner_of_object(object_):
    """
    Check if the current user is the owner of the given object.

    Raises an ForbiddenError in case the user is not owner of the object.

    :param object_:
    :return: None
    """
    if not g.user:
        raise UnauthorizedError("Authentication required.")
    if g.user.id != object_.created_by_id:
        if not g.user.is_superuser:
            raise ForbiddenError(
                "This is a private object. You should be the owner to modify!"
            )


def get_query_with_permissions(model, hide_archived=True):
    """
    Filter a model query for those data that the user is allowed to see.

    :param model:
    :return set: queryset for the model
    """
    query = db.session.query(model)
    if g.user is None:
        query = query.filter_by(is_public=True)
    else:
        if not g.user.is_superuser:
            user_id = g.user.id
            query = query.filter(
                or_(
                    and_(
                        model.is_private,
                        model.created_by_id == user_id,
                    ),
                    or_(
                        model.is_public,
                        model.is_internal,
                    ),
                )
            )
    if hide_archived:
        query = query.filter_by(archived=False)
    return query


def get_es_query_with_permissions(hide_archived=True):
    """
    Filter a model query for those data that the user is allowed to see.

    :return set: queryset for the model
    """

    def just_permissions():
        if g.user is None:
            return TermEqualsExactStringFilter("is_public", True)
        if not g.user.is_superuser:
            user_id = g.user.id
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

    permission_filter = just_permissions()
    if not hide_archived:
        return permission_filter
    archived_filter = TermEqualsExactStringFilter("archived", False)
    if permission_filter:
        return AndFilter([permission_filter, archived_filter])
    return archived_filter


def check_post_permission():
    """
    Check if a user has the permission to assign a group to the object.

    It also forbids to assign private objects to a group.
    """
    if not g.user:
        raise UnauthorizedError("Authentication required.")
    attributes = request.get_json()["data"]["attributes"]
    is_private = attributes["is_private"]
    group_ids = attributes["group_ids"] if "group_ids" in attributes else []
    if is_private:
        if group_ids:
            raise ConflictError("Private object can not be assigned to a group.")
    else:
        if not group_ids:
            raise ConflictError("Should be assigned to a group.")
        if not g.user.is_superuser:
            if not is_user_in_a_group(group_ids):
                raise ConflictError(
                    "User is not part of this group to assign it to the object."
                )


def check_patch_permission(data, object_to_patch):
    """
    Check if a user has the permission to patch an object.

    :param data:
    :param object_to_patch:
    """
    object_ = db.session.query(object_to_patch).filter_by(id=data["id"]).one_or_none()
    if object_ and object_.archived:
        raise ConflictError("It is not possible to change archived objects")
    if not is_superuser():
        if object_:
            if object_.is_private:
                assert_current_user_is_superuser_or_owner_of_object(object_)
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
    Check if a user has the permission to delete an object.

    :param kwargs:
    :param object_to_delete:
    """
    object_ = (
        db.session.query(object_to_delete).filter_by(id=kwargs["id"]).one_or_none()
    )
    if getattr(object_, "persistent_identifier", None):
        raise ConflictError("Deletion of objects with PID is not possible")
    if not is_superuser():
        if getattr(object_, "is_private", False):
            assert_current_user_is_superuser_or_owner_of_object(object_)
        else:
            raise ForbiddenError("User is not allowed to delete")


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
    if not g.user:
        raise UnauthorizedError("Authentication required.")
    if not g.user.is_superuser:
        if object_.created_by_id != g.user.id:
            raise ForbiddenError("User is not allowed to view object.")


def check_for_permission(model_class, kwargs):
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
            if not g.user:
                raise UnauthorizedError("Authentication required.")
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
            set_group_ids = set(
                group_ids or []
            )  # Could be None, so we need the or case
            deleted_elements = list(set_group_ids - set(changed_group))
            if deleted_elements:
                for element in deleted_elements:
                    if not is_user_admin_in_a_group([element]):
                        raise ForbiddenError(
                            "Only admins in a group are allowed to remove it."
                        )


def check_permissions_for_related_objects(model_class, id_):
    """
    Check if a user has the permission to view a related object.

    It does that by checking the main object permission (device/platform).

    :param id_:
    :param model_class: class model
    """
    object_ = db.session.query(model_class).filter_by(id=id_).first()
    if object_ is None:
        raise ObjectNotFound("Object not found!")
    related_object = object_.get_parent()
    if related_object.is_private:
        assert_current_user_is_superuser_or_owner_of_object(related_object)
    elif not related_object.is_public:
        if not g.user:
            raise UnauthorizedError("Authentication required.")


def check_post_permission_for_related_objects():
    """Check if a user has the permission to patch a related object."""
    data = decode_json_request_data()
    related_object = None
    if "device" in data["relationships"]:
        object_id = data["relationships"]["device"]["data"]["id"]
        related_object = db.session.query(Device).filter_by(id=object_id).one_or_none()
    if "platform" in data["relationships"]:
        object_id = data["relationships"]["platform"]["data"]["id"]
        related_object = (
            db.session.query(Platform).filter_by(id=object_id).one_or_none()
        )
    if related_object is None:
        raise ObjectNotFound("Object not found!")
    if related_object.archived:
        raise ConflictError("Posting for archived entity is not allowed")
    if not is_superuser():
        if related_object.is_private:
            assert_current_user_is_superuser_or_owner_of_object(related_object)
        else:
            group_ids = related_object.group_ids
            if not is_user_in_a_group(group_ids):
                raise ForbiddenError(
                    "User is not part of any group to edit this object."
                )


def check_patch_and_delete_permission_for_related_objects(data, object_to_patch):
    """
    Check if a user has the permission to patch a related object.

    :param data:
    :param object_to_patch:
    """
    object_ = db.session.query(object_to_patch).filter_by(id=data["id"]).one_or_none()
    if object_ is None:
        raise ObjectNotFound("Object not found!")
    related_object = object_.get_parent()
    if related_object.archived:
        raise ConflictError("Not possible to modify entries for archived entities")
    if not is_superuser():
        if related_object.is_private:
            assert_current_user_is_superuser_or_owner_of_object(related_object)
        else:
            group_ids = related_object.group_ids
            if not is_user_in_a_group(group_ids):
                raise ForbiddenError(
                    "User is not part of any group to edit this object."
                )


def get_query_with_permissions_for_related_objects(model):
    """
    Return the query for elements that depends on platform / devices permissions.

    It retrieves a collection of related objects through sqlalchemy by
    checking the permission of the platform / device.

    :param model:
    :return set: list of objects
    """
    query = db.session.query(model)
    if hasattr(model, "device"):
        related_object = model.device
    else:
        related_object = model.platform
    if g.user is None:
        query = query.filter(related_object.has(is_public=True))
    else:
        if not g.user.is_superuser:
            query = query.filter(
                or_(
                    related_object.has(is_public=True),
                    related_object.has(is_internal=True),
                    and_(
                        related_object.has(is_private=True),
                        related_object.has(created_by_id=g.user.id),
                    ),
                )
            )

    return query


def get_query_with_permissions_for_configuration_related_objects(model):
    """
    Return the query for elements that depend on configuration permissions.

    It retrieves a collection of related objects of a configuration
    through sqlalchemy by checking the object permission.

    :param model:
    :return set: list of objects
    """
    query = db.session.query(model)

    related_object = model.configuration
    if g.user is None:
        query = query.filter(related_object.has(is_public=True))
    else:
        if not g.user.is_superuser:
            query = query.filter(
                or_(
                    related_object.has(is_public=True),
                    related_object.has(is_internal=True),
                )
            )

    return query


def check_permissions_for_configuration_related_objects(model_class, id_):
    """
    Check if user has the permission to view related object.

    This depends on the permissions of the configuration.

    :param id_:
    :param model_class: class model
    """
    object_ = db.session.query(model_class).filter_by(id=id_).first()
    if object_ is None:
        raise ObjectNotFound("Object not found!")
    related_object = object_.configuration
    if not related_object.is_public:
        if not g.user:
            raise UnauthorizedError("Authentication required.")


def cfg_permission_group_defined(group_id):
    """Return true if the permission group is defined."""
    # Due to the database this can be the value if it is undefined.
    if group_id == "{}":
        return False
    return group_id


def check_post_permission_for_configuration_related_objects():
    """Check if a user has the permission to patch a related object of a configuration."""
    data = decode_json_request_data()
    object_id = data["relationships"]["configuration"]["data"]["id"]
    configuration = (
        db.session.query(Configuration).filter_by(id=object_id).one_or_none()
    )
    if configuration is None:
        raise ObjectNotFound("Object not found!")
    if configuration.archived:
        raise ConflictError("Posting for archived entities is not allowed")
    if not is_superuser():
        group_id = configuration.cfg_permission_group
        if cfg_permission_group_defined(group_id):
            if not is_user_in_a_group([group_id]):
                raise ForbiddenError(
                    "User is not part of the configuration-group to edit this object."
                )


def check_patch_permission_for_configuration_related_objects(data, object_to_patch):
    """
    Check if a user has the permission to patch a related object to a configuration.

    :param data:
    :param object_to_patch:
    """
    object_ = db.session.query(object_to_patch).filter_by(id=data["id"]).one_or_none()
    if object_ is None:
        raise ObjectNotFound("Object not found!")
    configuration = object_.get_parent()
    if configuration.archived:
        raise ConflictError("Patching for archived entities is not allowed")
    if not is_superuser():
        group_id = configuration.cfg_permission_group
        if cfg_permission_group_defined(group_id):
            if not is_user_in_a_group([group_id]):
                raise ForbiddenError(
                    "User is not part of the configuration-group to edit this object."
                )


def check_deletion_permission_for_configuration_related_objects(
    kwargs, object_to_delete
):
    """
    Check if a user has the permission to delete related object to a configuration.

    Note: both Member and Admin in a group should have the right
    to make the deletion.

    :param kwargs:
    :param object_to_delete:
    """
    object_ = (
        db.session.query(object_to_delete).filter_by(id=kwargs["id"]).one_or_none()
    )
    if object_ is None:
        raise ObjectNotFound("Object not found!")
    configuration = object_.get_parent()
    if configuration.archived:
        raise ConflictError("Deleting for archived entities is not allowed")
    if not is_superuser():
        group_id = configuration.cfg_permission_group
        if cfg_permission_group_defined(group_id):
            if not is_user_in_a_group([group_id]):
                raise ForbiddenError(
                    "User is not part of the configuration-group to delete this object."
                )


def check_parent_group_before_change_a_relationship(
    string_to_split_after, parent_model
):
    """
    Run checks to ensure that the user can edit the relationship.

    It checks the status of the main associated element
    (device, platform, configuration).

    :param parent_model:
    :param string_to_split_after:
    :return:
    """
    parent_id = request.path.split(string_to_split_after)[1][0]
    parent = db.session.query(parent_model).filter_by(id=parent_id).one_or_none()
    if parent_model == Configuration:
        group_ids = [parent.cfg_permission_group]
    else:
        group_ids = parent.group_ids
    if not is_user_in_a_group(group_ids):
        raise ForbiddenError("User is not part of any group to edit this object.")
