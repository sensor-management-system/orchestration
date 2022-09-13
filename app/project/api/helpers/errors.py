"""Common error classes to work with in the app."""

import json
from typing import Union

from flask import make_response
from flask_rest_jsonapi import JsonApiException
from flask_rest_jsonapi.errors import jsonapi_errors


class ErrorResponse(JsonApiException):
    """
    A class for handling json-api errors.

    Inspired by the JsonApiException class of `flask-rest-jsonapi` itself.
    # https://blog.fossasia.org/modifying-flask-rest-jsonapi-exception-handling-in-open-event-server-to-enable-support-for-sentry/
    """

    headers = {"Content-Type": "application/vnd.api+json"}

    def __init__(self, source: Union[dict, str], detail=None, title=None, status=None):
        """
        Initialize a jsonapi ErrorResponse object.

        :param dict source: the source of the error
        :param str detail: the detail of the error
        """
        if isinstance(source, str) and detail is None:
            # We have been passed a single argument, and hence source is unknown
            # so we'll represent source as detail
            super().__init__(None, source)
        else:
            super().__init__(source, detail, title, status)

    def respond(self):
        """
        Create a response (json:api style).

        :return: a jsonapi compliant response object
        """
        dict_ = self.to_dict()
        return make_response(
            json.dumps(jsonapi_errors([dict_])), self.status, self.headers
        )


class UnauthorizedError(ErrorResponse):
    """Default class for 401 Error."""

    title = "Unauthorized"
    status = 401


class AuthenticationFailedError(ErrorResponse):
    """Indication for an failed authentication (403)."""

    title = "Authentication failed"
    status = 403


class ForbiddenError(ErrorResponse):
    """Default class for 403 Error."""

    title = "Access Forbidden"
    status = 403


class NotFoundError(ErrorResponse):
    """Default class for 404 Error."""

    title = "Not Found"
    status = 404


class BadRequestError(ErrorResponse):
    """Default class for 400 Error."""

    status = 400
    title = "Bad Request"


class ConflictError(ErrorResponse):
    """Default class for 409 Error."""

    title = "Conflict"
    status = 409


class MethodNotAllowed(ErrorResponse):
    """Default Class to throw HTTP 405 Exception."""

    title = "Method Not Allowed"
    status = 405


class DeletionError(ErrorResponse):
    """
    Error class to indicate that an object can't be deleted.

    Especially when foreign keys still point to the object that
    should be deleted.
    """

    status = 409
    title = "Deletion failed as the object is still in use."


class UnsupportedMediaTypeError(ErrorResponse):
    """Default Class to throw HTTP 405 Exception extinction."""

    title = "Unsupported Media Type"
    status = 415


class ServiceIsUnreachableError(ErrorResponse):
    """Default Class to throw HTTP 523 Exception extinction."""

    title = "Service Is Unreachable"
    status = 523
