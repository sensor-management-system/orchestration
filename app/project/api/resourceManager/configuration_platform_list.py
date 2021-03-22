from ..models.base_model import db
from ..models.configuration_platform import ConfigurationPlatform
from ..schemas.configuration_platform_schema import (
    ConfigurationPlatformSchema,
)
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class ConfigurationPlatformList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Devices or create one.
    """

    schema = ConfigurationPlatformSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": ConfigurationPlatform}
