from flask_rest_jsonapi import ResourceRelationship

from project.api.models.baseModel import db
from project.api.models.properties import Properties
from project.api.schemas.propertiesSchema import PropertiesSchema


class PropertiesRelationship(ResourceRelationship):
    schema = PropertiesSchema
    data_layer = {'session': db.session,
                  'model': Properties}
