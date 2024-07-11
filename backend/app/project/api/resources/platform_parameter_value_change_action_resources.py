# SPDX-FileCopyrightText:  2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Module for the platform parameter value change action resource classes."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Platform, PlatformParameter, PlatformParameterValueChangeAction
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.platform_parameter_value_change_action_schema import (
    PlatformParameterValueChangeActionSchema,
)
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_platform_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class PlatformParameterValueChangeActionList(ResourceList):
    """Resource class for the platform parameter value change action list."""

    def query(self, kwargs):
        """Return a possibly filtered query."""
        query_ = filter_visible(self.session.query(self.model))
        platform_id = kwargs.get("platform_id")
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
        """Run some hooks after posting the data."""
        platform_parameter_id = result[0]["data"]["relationships"][
            "platform_parameter"
        ]["data"]["id"]
        platform_parameter = (
            db.session.query(PlatformParameter)
            .filter_by(id=platform_parameter_id)
            .first()
        )
        if platform_parameter:
            platform_id = platform_parameter.platform_id
            msg = "create;platform parameter value change action"
            query_platform_set_update_description_and_update_pidinst(msg, platform_id)
        return result

    schema = PlatformParameterValueChangeActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformParameterValueChangeAction,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class PlatformParameterValueChangeActionDetail(ResourceDetail):
    """Resource class for the platform parameter value change action details."""

    def before_get(self, args, kwargs):
        """Run some hooks before getting the data."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some hooks before patching the data."""
        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some hooks after patching the data."""
        platform_parameter_id = result["data"]["relationships"]["platform_parameter"][
            "data"
        ]["id"]
        platform_parameter = (
            db.session.query(PlatformParameter)
            .filter_by(id=platform_parameter_id)
            .first()
        )
        if platform_parameter:
            platform_id = platform_parameter.platform_id
            msg = "update;platform parameter value change action"
            query_platform_set_update_description_and_update_pidinst(msg, platform_id)
        return result

    def before_delete(self, args, kwargs):
        """Run some hooks before deleting the data."""
        value_change_action = (
            db.session.query(PlatformParameterValueChangeAction)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if value_change_action is None:
            raise ObjectNotFound("Object not found!")
        msg = "delete;platform parameter value change action"
        platform_parameter = value_change_action.platform_parameter
        set_update_description_text_user_and_pidinst(platform_parameter.platform, msg)

    schema = PlatformParameterValueChangeActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformParameterValueChangeAction,
    }
    permission_classes = [DelegateToCanFunctions]
