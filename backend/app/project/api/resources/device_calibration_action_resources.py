# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Resource classes for device calibration actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models.base_model import db
from ..models.calibration_actions import DeviceCalibrationAction
from ..models.device import Device
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.calibration_actions_schema import DeviceCalibrationActionSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_device_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class DeviceCalibrationActionList(ResourceList):
    """List resource for device calibration actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to request."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific devices, for example).
        """
        query_ = filter_visible(self.session.query(self.model))
        device_id = view_kwargs.get("device_id")

        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(DeviceCalibrationAction.device_id == device_id)
        return query_

    def after_post(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["device"]["data"]["id"]
        msg = "create;calibration action"
        query_device_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = DeviceCalibrationActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceCalibrationAction,
        "methods": {"query": query, "before_create_object": before_create_object},
    }
    permission_classes = [DelegateToCanFunctions]


class DeviceCalibrationActionDetail(ResourceDetail):
    """Detail resource for device calibration action (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if device calibration action not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Add updated by user id to the data."""
        add_updated_by_id(data)

    def after_patch(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["device"]["data"]["id"]
        msg = "update;calibration action"
        query_device_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Update the update description of the device."""
        action = (
            db.session.query(DeviceCalibrationAction)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if action is None:
            raise ObjectNotFound("Object not found!")
        self.tasks_after_delete = []
        device = action.get_parent()
        msg = "delete;calibration action"

        def run_updates():
            """Set the update description & update external metadata for pidinst."""
            set_update_description_text_user_and_pidinst(device, msg)

        self.tasks_after_delete.append(run_updates)

    def after_delete(self, *args, **kwargs):
        """Run some hooks after deleting."""
        for task in self.tasks_after_delete:
            task()
        return super().after_delete(*args, **kwargs)

    schema = DeviceCalibrationActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceCalibrationAction,
    }
    permission_classes = [DelegateToCanFunctions]
