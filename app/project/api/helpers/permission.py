import click
import requests
from flask import current_app
from flask_jwt_extended import get_current_user

from .errors import ForbiddenError, ServiceIsUnreachableError


def is_user_in_a_group(object_groups):
    """
    Check if the current user is in the same group
    as the object regardless if it is admin or member.

    :param object_groups:
    :return:
    """
    if not object_groups:
        return True
    current_user = get_current_user()
    idl_groups = get_all_permission_group(current_user.subject)
    # idl_groups = test_groups_list
    groups = idl_groups[0]["administratedDataprojects"] + idl_groups[0]["memberedDataprojects"]
    user_groups = extract_groups_ids_as_list(groups)
    return any(map(lambda each: each in user_groups, object_groups))


def extract_groups_ids_as_list(groups):
    """
    Extract the groups ids from the groups list.

    Example:
    groups=['/dataprojects/api/dataprojects/2', '/dataprojects/api/dataprojects/1', '/dataprojects/api/dataprojects/3']
    extract_groups_ids_as_list(groups)
    >> [2, 1, 3]

    :param groups: list of strings, where the last character is the group id
    :return: list of integers
    """
    user_groups = []
    for group in groups:
        user_groups.append(int(group.split("/")[-1]))
    return user_groups


def is_user_admin_in_a_group(object_groups):
    """
    check if the current user is an admin in the same group
     as the object.

    :param object_groups: a list of ids
    :return:
    """
    if not object_groups:
        return True
    current_user = get_current_user()
    idl_groups = get_all_permission_group(current_user.subject)
    # idl_groups = test_groups_list
    groups = idl_groups[0]["administratedDataprojects"]
    user_groups = extract_groups_ids_as_list(groups)
    return any(map(lambda each: each in user_groups, object_groups))


def is_user_super_admin():
    """
    Check if current user is a super admin.

    :return: boolean
    """

    current_user = get_current_user()

    return True if current_user.is_superuser else False


def get_all_permission_group(user_subject):
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
            raise ForbiddenError("User is not assigned to any group")
        return json_obj
    except (requests.exceptions.ConnectionError, requests.Timeout):
        raise ServiceIsUnreachableError("IDL connection error. Please try again later")


def is_user_owner_of_this_object(object_):
    """
    Checks if the current user is the owner of the given object.

    :param object_:
    :return:
    """
    current_user_id = get_current_user().id
    click.secho(current_user_id)
    click.secho(object_.created_by_id)
    if current_user_id != object_.created_by_id:
        raise ForbiddenError(
            "This is a private object. You should be the owner to modify!"
        )

# test_groups_list = [
#     {
#         "id": 3,
#         "username": "testuser@ufz.de",
#         "displayName": "Test User (WKDV)",
#         "referencedIri": "/infra/api/v1/accounts/testuser",
#         "administratedDataprojects": ["/dataprojects/api/dataprojects/2"],
#         "memberedDataprojects": [
#             "/dataprojects/api/dataprojects/1",
#             "/dataprojects/api/dataprojects/3",
#         ],
#     }
# ]
