import requests
from flask import current_app
from flask_jwt_extended import get_current_user

from .errors import NotFoundError


def is_user_in_a_group(object_groups):
    """

    :param object_groups:
    :return:
    """
    if not object_groups:
        return True
    current_user = get_current_user()
    cached_groups = get_all_permission_group(current_user.subject)
    groups = cached_groups[0]["administratedDataprojects"] + cached_groups[0]["memberedDataprojects"]
    user_groups = extract_groups_ids_as_list(groups)
    return any(map(lambda each: each in user_groups, object_groups))


def extract_groups_ids_as_list(groups):
    user_groups = []
    for group in groups:
        user_groups.append(int(group.split("/")[-1]))
        return user_groups


def is_user_Admin_in_a_group(object_groups):
    """

    :param object_groups:
    :return:
    """
    if not object_groups:
        return True
    current_user = get_current_user()
    cached_groups = get_all_permission_group(current_user.subject)
    groups = cached_groups[0]["administratedDataprojects"]
    user_groups = extract_groups_ids_as_list(groups)
    return any(map(lambda each: each in user_groups, object_groups))


def is_user_super_admin():
    """

    :return:
    """

    current_user = get_current_user()

    return True if current_user.admin else False


def get_all_permission_group(user_subject):
    """

    :param user_subject:
    :return:
    """
    sms_idl_token = current_app.config['SMS_IDL_TOKEN']
    access_headers = {"Authorization": "Bearer {}".format(sms_idl_token), "Accept": "application/json"}
    idl_url = current_app.config['IDL_URL']
    url = f'{idl_url}?page=1&itemsPerPage=100&username_is={user_subject}'
    response = requests.get(
        url, headers=access_headers)
    json_obj = response.json()
    if not json_obj:
        raise NotFoundError("User is not assigned to any group")
    return json_obj
