"""Resource classes for device software update actions."""

from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models.base_model import db
from ..models.device import Device
from ..models.software_update_actions import DeviceSoftwareUpdateAction
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..resources.base_resource import (
    check_if_object_not_found,
    query_device_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
)
from ..schemas.software_update_action_schema import DeviceSoftwareUpdateActionSchema
from ..token_checker import token_required


class DeviceSoftwareUpdateActionList(ResourceList):
    """List resource for device software update actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
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
                query_ = query_.filter(
                    DeviceSoftwareUpdateAction.device_id == device_id
                )
        return query_

    def after_post(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["device"]["data"]["id"]
        msg = "create;software update action"
        query_device_and_set_update_description_text(msg, result_id)

        return result

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
    permission_classes = [DelegateToCanFunctions]


class DeviceSoftwareUpdateActionDetail(ResourceDetail):
    """Detail resource for device software update actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceSoftwareUpdateAction not found."""
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
        msg = "update;software update action"
        query_device_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Update the update description of the device."""
        action = (
            db.session.query(DeviceSoftwareUpdateAction)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if action is None:
            raise ObjectNotFound("Object not found!")
        device = action.get_parent()
        msg = "delete;software update action"
        set_update_description_text_and_update_by_user(device, msg)

    schema = DeviceSoftwareUpdateActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceSoftwareUpdateAction,
    }
    permission_classes = [DelegateToCanFunctions]
