"""Resource classes for device software update actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.models.software_update_actions import DeviceSoftwareUpdateAction
from project.api.resourceManager.base_resource import (
    add_created_by_id,
    add_updated_by_id,
)
from project.api.schemas.software_update_action_schema import (
    DeviceSoftwareUpdateActionSchema,
)
from project.api.token_checker import token_required
from project.frj_csv_export.resource import ResourceList


class DeviceSoftwareUpdateActionList(ResourceList):
    """List resource for device software update actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
        """
        query_ = self.session.query(DeviceSoftwareUpdateAction)
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
                query_ = query_.filter(
                    DeviceSoftwareUpdateAction.device_id == device_id
                )
        return query_

    schema = DeviceSoftwareUpdateActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceSoftwareUpdateAction,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
        },
    }


class DeviceSoftwareUpdateActionDetail(ResourceDetail):
    """Detail resource for device software update actions (get, delete, patch)."""

    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data."""
        add_updated_by_id(data)

    schema = DeviceSoftwareUpdateActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceSoftwareUpdateAction,
    }


class DeviceSoftwareUpdateActionRelationship(ResourceRelationship):
    """Relationship resource for device software update actions."""

    schema = DeviceSoftwareUpdateActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceSoftwareUpdateAction,
    }
