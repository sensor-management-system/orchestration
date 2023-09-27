# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resource classes for the user handling."""

from flask_rest_jsonapi import ResourceDetail, ResourceList

from ..helpers.errors import MethodNotAllowed
from ..models.base_model import db
from ..models.user import User
from ..schemas.user_schema import UserSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


class UserList(ResourceList):
    """
    User list resource.

    Provides get and post methods to retrieve a
    collection of users or create one.
    """

    def before_post(self, args, kwargs, data=None):
        """Don't allow the post."""
        raise MethodNotAllowed("This endpoint is readonly!")

    schema = UserSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": User}


class UserDetail(ResourceDetail):
    """
    User detail resource.

    Provides get, patch and delete methods to retrieve details
    of an object, update an user and delete a user.
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if user not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data=None):
        """Don't allow patch requests."""
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_delete(self, args, kwargs):
        """Don't allow delete requests."""
        raise MethodNotAllowed("This endpoint is readonly!")

    schema = UserSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": User,
    }
