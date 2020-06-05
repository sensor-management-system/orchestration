from flask_rest_jsonapi import ResourceList

from project.api.models.base_model import db
from project.api.models.properties import Properties
from project.api.schemas.properties_schema import PropertiesSchema
from project.api.token_checker import token_required


class PropertiesList(ResourceList):
    """
    provides get and post methods to retrieve a
    collection of Platforms or create one.
    """
    schema = PropertiesSchema
    decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Properties}
