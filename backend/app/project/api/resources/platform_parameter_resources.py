# SPDX-FileCopyrightText:  2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Module for the platform parameter resource classes."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..helpers.errors import DeletionError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Platform, PlatformParameter
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.platform_parameter_schema import PlatformParameterSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_platform_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class PlatformParameterList(ResourceList):
    """Resource class for the platform parameter list."""

    def query(self, view_kwargs):
        """Return a (possibly) filtered query."""
        query_ = filter_visible(self.session.query(self.model))
        platform_id = view_kwargs.get("platform_id")
        if platform_id is not None:
            platform = self.session.query(Platform).filter_by(id=platform_id).first()
            if not platform:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Platform: {} not found".format(platform_id),
                )
            query_ = query_.filter(PlatformParameter.platform_id == platform_id)

        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Run some hooks before creating the object."""
        add_created_by_id(data)

    def after_post(self, result):
        """Run some hook after posting the data."""
        result_id = result[0]["data"]["relationships"]["platform"]["data"]["id"]
        msg = "create;platform parameter"
        query_platform_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = PlatformParameterSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformParameter,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class PlatformParameterDetail(ResourceDetail):
    """Resource class for the platform parameters."""

    def before_get(self, args, kwargs):
        """Run some hooks before getting the data."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some hooks before patching the data."""
        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some hooks after patching the data."""
        result_id = result["data"]["relationships"]["platform"]["data"]["id"]
        msg = "update;platform parameter"
        query_platform_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Run some hooks before deleting the data."""
        platform_paramater = (
            db.session.query(PlatformParameter).filter_by(id=kwargs["id"]).one_or_none()
        )
        if platform_paramater is None:
            raise ObjectNotFound("Object not found!")
        if platform_paramater.platform_parameter_value_change_actions:
            raise DeletionError("There are values associated to the parameter.")
        msg = "delete;platform parameter"
        set_update_description_text_user_and_pidinst(platform_paramater.platform, msg)

    schema = PlatformParameterSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformParameter,
    }
    permission_classes = [DelegateToCanFunctions]
