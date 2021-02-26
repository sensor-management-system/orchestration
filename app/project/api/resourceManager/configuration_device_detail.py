from flask_rest_jsonapi import ResourceDetail

from project.api.models.base_model import db
from project.api.models.configuration_device import ConfigurationDevice
from project.api.schemas.configuration_device_schema import ConfigurationDeviceSchema
from project.api.token_checker import token_required


class ConfigurationDeviceDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a configuration device
    """

    schema = ConfigurationDeviceSchema
    decorators = (token_required,)

    data_layer = {"session": db.session, "model": ConfigurationDevice}
