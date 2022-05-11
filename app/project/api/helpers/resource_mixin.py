import json
from json import JSONDecodeError

from flask import request

from ..auth.flask_openidconnect import open_id_connect
from ..helpers.errors import BadRequestError


def add_created_by_id(data):
    """
    Use jwt to add user id to dataset.
    :param data:
    :param args:
    :param kwargs:
    :return:

    .. note:: every HTTP-Methode should come with a json web token, which automatically
    check if the user exists or add the user to the database
    so that a user can't be None. Due to that created_by_id can't be None also.
    """
    user_entry = request.user
    if user_entry:
        data["created_by_id"] = user_entry.id


def add_updated_by_id(data):
    """
    Use jwt to add user id to dataset after updating the data.
    :param data:
    :param args:
    :param kwargs:
    :return:

    """
    user_entry = request.user
    if user_entry:
        data["updated_by_id"] = user_entry.id


def decode_json_request_data():
    try:
        data = json.loads(request.data.decode())["data"]
    except JSONDecodeError as e:
        raise BadRequestError(repr(e))
    return data
