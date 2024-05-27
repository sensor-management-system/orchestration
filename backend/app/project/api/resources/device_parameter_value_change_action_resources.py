# SPDX-FileCopyrightText:  2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Module for the device parameter value change action resource classes."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Device, DeviceParameter, DeviceParameterValueChangeAction
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.device_parameter_value_change_action_schema import (
    DeviceParameterValueChangeActionSchema,
)
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_device_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class DeviceParameterValueChangeActionList(ResourceList):
    """Resource class for the device parameter value change action list."""

    def query(self, kwargs):
        """Return a possibly filtered query."""
        query_ = filter_visible(self.session.query(self.model))
        device_id = kwargs.get("device_id")
        if device_id is not None:
            device = self.session.query(Device).filter_by(id=device_id).first()
            if not device:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device: {} not found".format(device_id),
                )
            query_ = query_.filter(DeviceParameter.device_id == device_id)
        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Run some hooks before creating the object."""
        add_created_by_id(data)

    def after_post(self, result):
        """Run some hooks after posting the data."""
        device_parameter_id = result[0]["data"]["relationships"]["device_parameter"][
            "data"
        ]["id"]
        device_parameter = (
            db.session.query(DeviceParameter).filter_by(id=device_parameter_id).first()
        )
        if device_parameter:
            device_id = device_parameter.device_id
            msg = "create;device parameter value change action"
            query_device_set_update_description_and_update_pidinst(msg, device_id)
        return result

    schema = DeviceParameterValueChangeActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceParameterValueChangeAction,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class DeviceParameterValueChangeActionDetail(ResourceDetail):
    """Resource class for the device parameter value change action details."""

    def before_get(self, args, kwargs):
        """Run some hooks before getting the data."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some hooks before patching the data."""
        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some hooks after patching the data."""
        device_parameter_id = result["data"]["relationships"]["device_parameter"][
            "data"
        ]["id"]
        device_parameter = (
            db.session.query(DeviceParameter).filter_by(id=device_parameter_id).first()
        )
        if device_parameter:
            device_id = device_parameter.device_id
            msg = "update;device parameter value change action"
            query_device_set_update_description_and_update_pidinst(msg, device_id)
        return result

    def before_delete(self, args, kwargs):
        """Run some hooks before deleting the data."""
        value_change_action = (
            db.session.query(DeviceParameterValueChangeAction)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if value_change_action is None:
            raise ObjectNotFound("Object not found!")
        msg = "delete;device parameter value change action"
        device_parameter = value_change_action.device_parameter
        set_update_description_text_user_and_pidinst(device_parameter.device, msg)

    schema = DeviceParameterValueChangeActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceParameterValueChangeAction,
    }
    permission_classes = [DelegateToCanFunctions]
