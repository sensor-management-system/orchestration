from flask_rest_jsonapi import ResourceList

from project.api.models.base_model import db
from project.api.models.device_property import DeviceProperty
from project.api.schemas.device_property_schema import DevicePropertySchema
from project.api.token_checker import token_required


class DevicePropertyList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Devices or create one.
    """

    schema = DevicePropertySchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceProperty}
