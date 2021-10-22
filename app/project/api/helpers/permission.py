import json

import requests
from flask import current_app
from flask_jwt_extended import get_current_user

from .errors import ForbiddenError, ServiceIsUnreachableError
from ..models.idl_user import idl_from_dict


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
    idl_groups = get_all_permission_groups(current_user.subject)
    user_groups = idl_groups.administrated_permissions_groups + idl_groups.membered_permissions_groups
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
    idl_groups = get_all_permission_groups(current_user.subject)
    user_groups = idl_groups.administrated_permissions_groups
    return any(group in user_groups for group in groups_to_check)


def is_user_super_admin():
    """
    Check if current user is a super admin.

    :return: boolean
    """

    current_user = get_current_user()

    return current_user.is_superuser


def get_all_permission_groups(user_subject):
    """
    Returns a list of groups or Projects for a user-subject that are fetched from the IDL service.

    :param user_subject:
    :return:
    """
    sms_idl_token = current_app.config["SMS_IDL_TOKEN"]
    access_headers = {
        "Authorization": "Bearer {}".format(sms_idl_token),
        "Accept": "application/json",
    }
    idl_url = current_app.config["IDL_URL"]
    url = f"{idl_url}?page=1&itemsPerPage=100&username_is={user_subject}"
    try:
        response = requests.get(url, headers=access_headers)
        json_obj = response.json()
        if not json_obj:
            json_obj = '[]'
        result = idl_from_dict(json.loads(json_obj))
        return result[0]
    except (requests.exceptions.ConnectionError, requests.Timeout):
        raise ServiceIsUnreachableError("IDL connection error. Please try again later")


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
