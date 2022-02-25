"""Resource classes for device unmount actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.device import Device
from ..models.unmount_actions import DeviceUnmountAction
from ..schemas.unmount_actions_schema import DeviceUnmountActionSchema
from ..token_checker import token_required


class DeviceUnmountActionList(ResourceList):
    """List resource for the device unmount actions (get, post)."""

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
        """
        query_ = self.session.query(DeviceUnmountAction)
        configuration_id = view_kwargs.get("configuration_id")
        device_id = view_kwargs.get("device_id")
        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id",},
                    "Configuration: {} not found".format(configuration_id),
                )
            else:
                query_ = query_.filter(
                    DeviceUnmountAction.configuration_id == configuration_id
                )
        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id",}, "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(DeviceUnmountAction.device_id == device_id)
        return query_

    schema = DeviceUnmountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceUnmountAction,
        "methods": {"query": query,},
    }


class DeviceUnmountActionDetail(ResourceDetail):
    """Detail resource for device unmount actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceUnmountAction not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = DeviceUnmountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceUnmountAction,
    }


class DeviceUnmountActionRelationship(ResourceRelationship):
    """Relationship resource for device unmount actions."""

    schema = DeviceUnmountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceUnmountAction,
    }
