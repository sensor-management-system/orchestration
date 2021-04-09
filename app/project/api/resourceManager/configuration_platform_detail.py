from flask_rest_jsonapi import ResourceDetail

from ..models.base_model import db
from ..models.configuration_platform import ConfigurationPlatform
from ..schemas.configuration_platform_schema import ConfigurationPlatformSchema
from ..token_checker import token_required


class ConfigurationPlatformDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a configuration platform
    """

    schema = ConfigurationPlatformSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": ConfigurationPlatform}
