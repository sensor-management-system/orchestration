# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from flask_rest_jsonapi import ResourceDetail

from .base_resource import check_if_object_not_found
from ..helpers.errors import MethodNotAllowed
from ..models.base_model import db
from ..models.user import User
from ..schemas.user_schema import UserSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class UserList(ResourceList):
    """
    provides get and post methods to retrieve a
    collection of Events or create one.
    """

    def before_post(self, args, kwargs, data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    schema = UserSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": User}


class UserDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an Event and delete a Event
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if user not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_delete(self, args, kwargs):
        raise MethodNotAllowed("This endpoint is readonly!")

    schema = UserSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": User,
    }
