import json
from json import JSONDecodeError

from flask import g, request

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
    data["created_by_id"] = g.user.id
    add_updated_by_id(data)


def add_updated_by_id(data):
    """
    Use jwt to add user id to dataset after updating the data.
    :param data:
    :param args:
    :param kwargs:
    :return:

    """
    data["updated_by_id"] = g.user.id


def decode_json_request_data():
    try:
        data = json.loads(request.data.decode())["data"]
    except JSONDecodeError as e:
        raise BadRequestError(repr(e))
    return data
