"""Resource classes for device calibration actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import get_collection_with_permissions_for_related_objects
from .base_resource import check_if_object_not_found
from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.calibration_actions import DeviceCalibrationAction
from ..models.device import Device
from ..schemas.calibration_actions_schema import DeviceCalibrationActionSchema
from ..token_checker import token_required


class DeviceCalibrationActionList(ResourceList):
    """List resource for device calibration actions (get, post)."""

    def after_get_collection(self, collection, qs, view_kwargs):
        """Take the intersection between requested collection and
        what the user allowed querying.

        :param collection:
        :param qs:
        :param view_kwargs:
        :return:
        """

        return get_collection_with_permissions_for_related_objects(
            self.model, collection
        )

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific devices, for example).
        """
        query_ = self.session.query(DeviceCalibrationAction)
        device_id = view_kwargs.get("device_id")

        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id",}, "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(DeviceCalibrationAction.device_id == device_id)
        return query_

    schema = DeviceCalibrationActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceCalibrationAction,
        "methods": {"query": query, "after_get_collection": after_get_collection},
    }


class DeviceCalibrationActionDetail(ResourceDetail):
    """Detail resource for device calibration action (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if device calibration action not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = DeviceCalibrationActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceCalibrationAction,
    }


class DeviceCalibrationActionRelationship(ResourceRelationship):
    """Relationship resource for device calibration actions."""

    schema = DeviceCalibrationActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceCalibrationAction,
    }
