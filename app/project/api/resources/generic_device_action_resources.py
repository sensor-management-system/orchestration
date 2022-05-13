"""Resource classes for the generic device actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..helpers.errors import MethodNotAllowed
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models.base_model import db
from ..models.device import Device
from ..models.generic_actions import GenericDeviceAction
from ..resources.base_resource import check_if_object_not_found
from ..schemas.generic_actions_schema import GenericDeviceActionSchema
from ..token_checker import token_required


class GenericDeviceActionList(ResourceList):
    """List resource for generic device actions (get & post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific devices, for example).
        """
        query_ = get_query_with_permissions_for_related_objects(self.model)
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
                query_ = query_.filter(GenericDeviceAction.device_id == device_id)
        return query_

    schema = GenericDeviceActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericDeviceAction,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
        },
    }


class GenericDeviceActionDetail(ResourceDetail):
    """Detail resource for generic device actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if GenericDeviceAction not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Add updated by user id to the data."""
        add_updated_by_id(data)

    schema = GenericDeviceActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericDeviceAction,
    }


class GenericDeviceActionRelationship(ResourceRelationship):
    """Relationship resource for generic device actions."""

    schema = GenericDeviceActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericDeviceAction,
    }
