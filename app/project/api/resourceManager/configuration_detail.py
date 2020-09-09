from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.schemas.configuration_schema import ConfigurationSchema


class ConfigurationDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete a Device
    """

    schema = ConfigurationSchema
    # decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Configuration,
    }
