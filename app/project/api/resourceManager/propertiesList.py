from flask_rest_jsonapi import ResourceList

from project.api.models.baseModel import db
from project.api.models.properties import Properties
from project.api.schemas.propertiesSchema import PropertiesSchema


class PropertiesList(ResourceList):
    schema = PropertiesSchema
    data_layer = {'session': db.session,
                  'model': Properties}
