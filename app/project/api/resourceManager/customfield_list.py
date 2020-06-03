from flask_rest_jsonapi import ResourceList

from project.api.models.base_model import db
from project.api.schemas.customfield_schema import CustomFieldSchema
from project.api.models.customfield import CustomField


class CustomFieldList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of CustomFiels or create one.
    """
    schema = CustomFieldSchema
    data_layer = {'session': db.session,
                  'model': CustomField}
