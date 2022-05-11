"""Resource classes for device unmount actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..helpers.errors import MethodNotAllowed
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.device import Device
from ..models.unmount_actions import DeviceUnmountAction
from ..schemas.unmount_actions_schema import DeviceUnmountActionSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


class DeviceUnmountActionList(ResourceList):
    """List resource for the device unmount actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
        """
        query_ = get_query_with_permissions_for_related_objects(self.model)
        configuration_id = view_kwargs.get("configuration_id")
        device_id = view_kwargs.get("device_id")
        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
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
                    {
                        "parameter": "id",
                    },
                    "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(DeviceUnmountAction.device_id == device_id)
        return query_

    schema = DeviceUnmountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceUnmountAction,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
        },
    }


class DeviceUnmountActionDetail(ResourceDetail):
    """Detail resource for device unmount actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceUnmountAction not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Add updated by user id to the data."""
        add_updated_by_id(data)

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


class DeviceUnmountActionRelationshipReadOnly(DeviceUnmountActionRelationship):
    """A readonly relationship endpoint for device unmount actions."""

    def before_post(self, args, kwargs, json_data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_patch(self, args, kwargs, data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_delete(self, args, kwargs):
        raise MethodNotAllowed("This endpoint is readonly!")
