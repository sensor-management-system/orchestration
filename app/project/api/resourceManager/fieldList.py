from flask_rest_jsonapi import ResourceList

from project.api.models.baseModel import db
from project.api.schemas.fieldSchema import FieldSchema
from project.api.models.field import Field


class FieldList(ResourceList):
    schema = FieldSchema
    data_layer = {'session': db.session,
                  'model': Field}
