from flask_rest_jsonapi import ResourceDetail

from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.resourceManager.base_resource import add_updated_by_id
from project.api.schemas.configuration_schema import ConfigurationSchema
from project.api.token_checker import token_required


class ConfigurationDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data"""
        add_updated_by_id(data)

    schema = ConfigurationSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Configuration,
    }
