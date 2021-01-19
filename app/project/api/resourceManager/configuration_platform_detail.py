from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.configuration_platform import ConfigurationPlatform
from project.api.schemas.configuration_platform_schema import (
    ConfigurationPlatformSchema,
)
from project.api.token_checker import token_required


class ConfigurationPlatformDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    schema = ConfigurationPlatformSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationPlatform,
    }
