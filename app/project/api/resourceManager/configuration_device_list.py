from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.configuration_device import ConfigurationDevice
from ..schemas.configuration_device_schema import ConfigurationDeviceSchema
from ..token_checker import token_required


class ConfigurationDeviceList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Devices or create one.
    """

    schema = ConfigurationDeviceSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": ConfigurationDevice}
