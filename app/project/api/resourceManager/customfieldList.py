from flask_rest_jsonapi import ResourceList

from project.api.models.baseModel import db
from project.api.schemas.customfieldSchema import CustomFieldSchema
from project.api.models.customfield import CustomField


class CustomFieldList(ResourceList):
    schema = CustomFieldSchema
    data_layer = {'session': db.session,
                  'model': CustomField}
