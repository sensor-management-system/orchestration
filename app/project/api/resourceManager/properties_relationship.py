from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.properties import Properties
from project.api.schemas.properties_schema import PropertiesSchema


class PropertiesRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Properties and other objects.
    """
    schema = PropertiesSchema
    data_layer = {'session': db.session,
                  'model': Properties}
