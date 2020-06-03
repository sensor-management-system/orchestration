from flask_rest_jsonapi import ResourceList

from project.api.models.base_model import db
from project.api.models.properties import Properties
from project.api.schemas.properties_schema import PropertiesSchema


class PropertiesList(ResourceList):
    """
    provides get and post methods to retrieve a
    collection of Platforms or create one.
    """
    schema = PropertiesSchema
    data_layer = {'session': db.session,
                  'model': Properties}
