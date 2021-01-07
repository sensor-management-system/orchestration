from flask_rest_jsonapi import ResourceList
from project.api.models.base_model import db
from project.api.models.configuration_device import ConfigurationDevice
from project.api.schemas.configuration_device_schema import ConfigurationDeviceSchema
from project.api.token_checker import token_required


class ConfigurationDeviceList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Devices or create one.
    """

    schema = ConfigurationDeviceSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": ConfigurationDevice}
