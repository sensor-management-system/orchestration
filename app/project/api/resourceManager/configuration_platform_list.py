from project.frj_csv_export.resource import ResourceList
from project.api.models.base_model import db
from project.api.models.configuration_platform import ConfigurationPlatform
from project.api.schemas.configuration_platform_schema import (
    ConfigurationPlatformSchema,
)
from project.api.token_checker import token_required


class ConfigurationPlatformList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Devices or create one.
    """

    schema = ConfigurationPlatformSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": ConfigurationPlatform}
