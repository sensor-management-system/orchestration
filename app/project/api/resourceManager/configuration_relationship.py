from flask_rest_jsonapi import ResourceRelationship

from ..helpers.errors import MethodNotAllowed
from ..models.base_model import db
from ..models.configuration import Configuration
from ..schemas.configuration_schema import ConfigurationSchema
from ..token_checker import token_required


class ConfigurationRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Device and objects.
    """

    schema = ConfigurationSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": Configuration}


class ConfigurationRelationshipReadOnly(ConfigurationRelationship):
    """A readonly relationship endpoint for configurations."""

    def before_post(self, args, kwargs, json_data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_patch(self, args, kwargs, data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_delete(self, args, kwargs):
        raise MethodNotAllowed("This endpoint is readonly!")
