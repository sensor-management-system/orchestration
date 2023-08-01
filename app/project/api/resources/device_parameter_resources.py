# SPDX-FileCopyrightText:  2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Module for the device parameter resource classes."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..helpers.errors import DeletionError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Device, DeviceParameter
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.device_parameter_schema import DeviceParameterSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_device_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class DeviceParameterList(ResourceList):
    """Resource class for the device parameter list."""

    def query(self, view_kwargs):
        """Return a (possibly) filtered query."""
        query_ = filter_visible(self.session.query(self.model))
        device_id = view_kwargs.get("device_id")
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
        """Run some hook after posting the data."""
        result_id = result[0]["data"]["relationships"]["device"]["data"]["id"]
        msg = "create;device parameter"
        query_device_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = DeviceParameterSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceParameter,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class DeviceParameterDetail(ResourceDetail):
    """Resource class for the device parameters."""

    def before_get(self, args, kwargs):
        """Run some hooks before getting the data."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some hooks before patching the data."""
        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some hooks after patching the data."""
        result_id = result["data"]["relationships"]["device"]["data"]["id"]
        msg = "update;device parameter"
        query_device_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Run some hooks before deleting the data."""
        device_paramater = (
            db.session.query(DeviceParameter).filter_by(id=kwargs["id"]).one_or_none()
        )
        if device_paramater is None:
            raise ObjectNotFound("Object not found!")
        if device_paramater.device_parameter_value_change_actions:
            raise DeletionError("There are values associated to the parameter.")
        msg = "delete;device parameter"
        set_update_description_text_user_and_pidinst(device_paramater.device, msg)

    schema = DeviceParameterSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceParameter,
    }
    permission_classes = [DelegateToCanFunctions]
