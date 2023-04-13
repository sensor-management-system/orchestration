# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Some helper to have some easy class based views."""

from functools import wraps

from flask import request

from ...api.helpers.errors import ErrorResponse, MethodNotAllowed


def class_based_view(cls):
    """Allow us to wrap the requests in classes."""

    @wraps(cls)
    def wrapper(*args, **kwargs):
        return cls(*args, **kwargs)()

    return wrapper


class BaseView:
    """
    Base view that can be used for class based views.

    It provides a basic call method that dispatches into
    get, post, delete, put or patch requests.

    It works together with the class_based_view decorator.
    That means that it sets the args & kwargs for the flask route
    into the classes constructor.

    This base view also adds handling for error responses that
    we also use with the flask rest json api framework.
    """

    def __call__(self):
        """Run the request."""
        try:
            method_lookup = {
                "POST": self.post,
                "GET": self.get,
                "DELETE": self.delete,
                "PATCH": self.patch,
                "PUT": self.put,
            }
            handler = method_lookup.get(request.method)
            if handler:
                return handler()
            else:
                raise MethodNotAllowed("Method not allowed")
        except ErrorResponse as e:
            return e.respond()

    def post(self):
        """Run the post request."""
        raise MethodNotAllowed("Method not allowed")

    def get(self):
        """Run the get request."""
        raise MethodNotAllowed("Method not allowed")

    def put(self):
        """Run the put request."""
        raise MethodNotAllowed("Method not allowed")

    def patch(self):
        """Run the patch request."""
        raise MethodNotAllowed("Method not allowed")

    def delete(self):
        """Run the delete request."""
        raise MethodNotAllowed("Method not allowed")
