"""Module for the device property detail resource."""
from flask_rest_jsonapi import ResourceDetail

from .base_resource import check_if_object_not_found
from ..models.base_model import db
from ..models.device_property import DeviceProperty
from ..schemas.device_property_schema import DevicePropertySchema
from ..token_checker import token_required


class DevicePropertyDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceProperty not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = DevicePropertySchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceProperty,
    }
