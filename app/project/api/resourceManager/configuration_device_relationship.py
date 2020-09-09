from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.configuration_device import ConfigurationDevice
from project.api.schemas.configuration_device_schema import ConfigurationDeviceSchema
from project.api.token_checker import token_required


class ConfigurationDeviceRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Device and objects.
    """
    schema = ConfigurationDeviceSchema
    # decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': ConfigurationDevice}
