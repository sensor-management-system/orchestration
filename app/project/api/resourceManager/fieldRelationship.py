from flask_rest_jsonapi import ResourceRelationship

from project.api.models.baseModel import db
from project.api.schemas.fieldSchema import FieldSchema
from project.api.models.field import Field


class FieldRelationship(ResourceRelationship):
    schema = FieldSchema
    data_layer = {'session': db.session,
                  'model': Field}
