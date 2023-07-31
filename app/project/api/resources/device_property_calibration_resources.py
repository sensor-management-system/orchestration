# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resource classes for device property calibrations."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..models.base_model import db
from ..models.calibration_actions import (
    DeviceCalibrationAction,
    DevicePropertyCalibration,
)
from ..models.device import Device
from ..models.device_property import DeviceProperty
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..resources.base_resource import check_if_object_not_found
from ..schemas.calibration_actions_schema import DevicePropertyCalibrationSchema
from ..token_checker import token_required


class DevicePropertyCalibrationList(ResourceList):
    """List resource for device property calibrations (get, post)."""

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific devices, for example).
        """
        query_ = filter_visible(self.session.query(self.model))
        device_id = view_kwargs.get("device_id")
        device_calibration_action_id = view_kwargs.get("device_calibration_action_id")
        device_property_id = view_kwargs.get("device_property_id")

        if device_calibration_action_id is not None:
            try:
                self.session.query(DeviceCalibrationAction).filter_by(
                    id=device_calibration_action_id
                ).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "DeviceCalibrationAction: {} not found".format(
                        device_calibration_action_id
                    ),
                )
            else:
                query_ = query_.filter(
                    DevicePropertyCalibration.calibration_action_id
                    == device_calibration_action_id
                )
        if device_property_id is not None:
            try:
                self.session.query(DeviceProperty).filter_by(
                    id=device_property_id
                ).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "DeviceProperty: {} not found".format(device_property_id),
                )
            else:
                query_ = query_.filter(
                    DevicePropertyCalibration.device_property_id == device_property_id
                )
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
                # Due to the visible filter we already join with the
                # DevicePropertyCalibration
                query_ = query_.filter(DeviceCalibrationAction.device_id == device_id)

        return query_

    schema = DevicePropertyCalibrationSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DevicePropertyCalibration,
        "methods": {
            "query": query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class DevicePropertyCalibrationDetail(ResourceDetail):
    """Detail resource for the device property calibrations (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if DevicePropertyCalibration not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = DevicePropertyCalibrationSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DevicePropertyCalibration,
    }
    permission_classes = [DelegateToCanFunctions]
