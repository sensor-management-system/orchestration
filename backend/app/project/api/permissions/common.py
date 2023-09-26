# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Some common permission classes that can be combined with others."""

from flask import g, request
from marshmallow.exceptions import ValidationError

from .base import BasePermission, ModelPermission
from .rules import can_change, can_create, can_delete, can_edit, can_see


class AllowAny(BasePermission):
    """Implementation to allow any request."""

    def has_permission(self, view, view_args, view_kwargs, *args, **kwargs):
        """Return true in any case."""
        return True


class IsAuthenticated(BasePermission):
    """Check for authentification."""

    def has_permission(self, view, view_args, view_kwargs, *args, **kwargs):
        """Return true if we have a user."""
        if g.user:
            return True
        return False


class IsReadOnly(BasePermission):
    """Check for readonly requests."""

    def has_permission(self, view, view_args, view_kwargs, *args, **kwargs):
        """Return true if it is a reuest that only reads."""
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return False


class IsSuperUser(BasePermission):
    """Check for a super user."""

    def has_permission(self, view, view_args, view_kwargs, *args, **kwargs):
        """Return true if the request was made from a superuser."""
        if g.user and g.user.is_superuser:
            return True
        return False


class IsPost(BasePermission):
    """Check for post requests."""

    def has_permission(self, view, view_args, view_kwargs, *args, **kwargs):
        """Return true if it is a post request."""
        return request.method == "POST"


class IsPatch(BasePermission):
    """Check for patch requests."""

    def has_permission(self, view, view_args, view_kwargs, *args, **kwargs):
        """Return true if it is a patch request."""
        return request.method == "PATCH"


class IsDelete(BasePermission):
    """Check for  delete requests."""

    def has_permission(self, view, view_args, view_kwargs, *args, **kwargs):
        """Return true if it is a delete requests."""
        return request.method == "DELETE"


class DelegateToCanFunctions(ModelPermission):
    """
    Check to delegate to the can_see, can_create, etc functions.

    The processed entity must be supported here.
    """

    def has_object_permission(self, view, view_args, view_kwargs, obj, *args, **kwargs):
        """Return that the can_see, etc functions decides - depended on the request."""
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return can_see(obj)
        if request.method in ["PATCH"]:
            editable = can_edit(obj)
            if not editable:
                return False
            try:
                data = view_args[0].schema().load(request.json, partial=True)
                return can_change(obj, data)
            except ValidationError:
                # This will be handled by other parts of the application.
                # So we don't care here.
                return True
        if request.method in ["DELETE"]:
            return can_delete(obj)

    def has_create_permission(
        self, view, view_args, view_kwargs, data, *args, **kwargs
    ):
        """Return true if we can create for our model."""
        resource = view_args[0]
        data_layer = resource.data_layer
        model = data_layer["model"]
        return can_create(model, data)
