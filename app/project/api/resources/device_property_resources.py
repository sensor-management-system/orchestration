"""Module for the device property list resource."""
from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..models.base_model import db
from ..models.device import Device
from ..models.device_property import DeviceProperty
from ..schemas.device_property_schema import DevicePropertySchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_device_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
)


class DevicePropertyList(ResourceList):
    """
    List resource for device properties.

    Provides get and post methods to retrieve
    a collection of device properties or create one.
    """

    def query(self, view_kwargs):
        """
        Query all the entries from the database.

        Also handle cases to search for all the device
        properties of a specific device.
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
                query_ = query_.filter(DeviceProperty.device_id == device_id)
        return query_

    def after_post(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["device"]["data"]["id"]
        msg = "create;measured quantity"
        query_device_and_set_update_description_text(msg, result_id)

        return result

    schema = DevicePropertySchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceProperty,
        "methods": {"query": query},
    }


"""Module for the device property detail resource."""


class DevicePropertyDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceProperty not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def after_patch(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["device"]["data"]["id"]
        msg = "update;measured quantity"
        query_device_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        device_property = (
            db.session.query(DeviceProperty).filter_by(id=kwargs["id"]).one_or_none()
        )
        if device_property is None:
            raise ObjectNotFound("Object not found!")
        device = device_property.get_parent()
        msg = "delete;measured quantity"
        set_update_description_text_and_update_by_user(device, msg)

    schema = DevicePropertySchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceProperty,
    }
