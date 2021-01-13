from flask_rest_jsonapi import ResourceDetail

from project.api.models.base_model import db
from project.api.models.device_property import DeviceProperty
from project.api.schemas.device_property_schema import DevicePropertySchema
from project.api.token_checker import token_required


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
