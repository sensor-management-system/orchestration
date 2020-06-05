from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.properties import Properties
from project.api.schemas.properties_schema import PropertiesSchema
from project.api.token_checker import token_required


class PropertiesDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Platform
    """

    schema = PropertiesSchema
    decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Properties
                  }
