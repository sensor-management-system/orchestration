from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.configuration_platform import ConfigurationPlatform
from project.api.schemas.configuration_platform_schema import (
    ConfigurationPlatformSchema,
)
from project.api.token_checker import token_required


class ConfigurationPlatformDetail(ResourceDetail):
    """
    provides get, patch and delete methods
    of an object, update and object and delete a configuration platform.
    """

    schema = ConfigurationPlatformSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": ConfigurationPlatform}
