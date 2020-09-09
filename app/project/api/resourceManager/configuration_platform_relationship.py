from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.configuration_platform import ConfigurationPlatform
from project.api.schemas.configuration_platform_schema import ConfigurationPlatformSchema
from project.api.token_checker import token_required


class ConfigurationPlatformRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Device and objects.
    """
    schema = ConfigurationPlatformSchema
    # decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': ConfigurationPlatform}
