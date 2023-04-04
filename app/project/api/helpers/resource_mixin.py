"""Some helper functions to be used in various resource classes."""

import json
from json import JSONDecodeError

from flask import g, request

from ..helpers.errors import BadRequestError


def add_created_by_id(data):
    """
    Use user object to add user id to dataset.

    :param data:
    :param args:
    :param kwargs:
    :return:

    .. note:: every HTTP-Methode should come with a json web token, which automatically
    check if the user exists or add the user to the database
    so that a user can't be None. Due to that created_by_id can't be None also.
    """
    data["created_by_id"] = g.user.id
    add_updated_by_id(data)


def add_updated_by_id(data):
    """
    Use user object to add user id to dataset after updating the data.

    :param data:
    :param args:
    :param kwargs:
    :return:

    """
    data["updated_by_id"] = g.user.id


def decode_json_request_data():
    """Try to decode the json data."""
    try:
        data = json.loads(request.data.decode())["data"]
    except JSONDecodeError as e:
        raise BadRequestError(repr(e))
    return data


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
