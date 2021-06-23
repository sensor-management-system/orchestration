from flask_rest_jsonapi import ResourceRelationship

from ..models.base_model import db
from ..models.configuration_platform import ConfigurationPlatform
from ..schemas.configuration_platform_schema import ConfigurationPlatformSchema
from ..token_checker import token_required


class ConfigurationPlatformRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Device and objects.
    """

    schema = ConfigurationPlatformSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": ConfigurationPlatform}
