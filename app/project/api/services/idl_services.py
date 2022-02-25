import requests
from flask import current_app

from ..helpers.errors import ServiceIsUnreachableError, ConflictError
from ..models.idl_user import idl_from_dict
from ..models.permission_groups import permission_groups_from_list_of_dicts


def make_request_to_idl(idl_url, params):
    """
    Make a request to the IDL.

    :param idl_url:
    :param params:
    :return:
    """
    sms_idl_token = current_app.config["SMS_IDL_TOKEN"]
    access_headers = {
        "Authorization": "Bearer {}".format(sms_idl_token),
        "Accept": "application/json",
    }
    try:
        response = requests.get(
            idl_url, headers=access_headers, params=params, timeout=5
        )
        response.raise_for_status()

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        raise ServiceIsUnreachableError(repr(e))
    except requests.exceptions.HTTPError as e:
        raise ConflictError(repr(e))
    json_obj = response.json()
    return json_obj


def get_permission_groups():
    """
    Returns a list of groups fetched from the IDL service.

    :return: list
    """
    idl_url = current_app.config["IDL_URL"]
    if idl_url:
        idl_url += "/permission-groups"
    params = {"page": 1, "itemsPerPage": 100}
    json_obj = make_request_to_idl(idl_url, params)
    if not json_obj:
        return []
    result = permission_groups_from_list_of_dicts(json_obj)
    return result


class Idl:
    def get_all_permission_groups_for_a_user(self, user_subject):
        """
        Returns a list of groups or Projects for a user-subject that are fetched from the IDL service.

        :param user_subject: the subject coming from the user jwt.
        :return: list
        """
        idl_url = current_app.config["IDL_URL"]
        if idl_url:
            idl_url += "/user-accounts"
        params = {"page": 1, "itemsPerPage": 100, "userName_is": user_subject}
        json_obj = make_request_to_idl(idl_url, params)
        # Checking for an empty list
        if not json_obj:
            return []
        result = idl_from_dict(json_obj[0])
        return result
