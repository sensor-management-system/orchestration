from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.schemas.configuration_schema import ConfigurationSchema
from project.api.token_checker import token_required


class ConfigurationRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Device and objects.
    """

    schema = ConfigurationSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": Configuration}
