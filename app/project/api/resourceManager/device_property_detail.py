"""Module for the device property detail resource."""
from flask_rest_jsonapi import ResourceDetail

from ..models.base_model import db
from ..models.device_property import DeviceProperty
from ..schemas.device_property_schema import DevicePropertySchema
from ..token_checker import token_required


class DevicePropertyDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    schema = DevicePropertySchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceProperty,
    }
