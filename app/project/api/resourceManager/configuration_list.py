from project.frj_csv_export.resource import ResourceList
from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.schemas.configuration_schema import ConfigurationSchema
from project.api.datalayers.esalchemy import EsSqlalchemyDataLayer
from project.api.token_checker import token_required


class ConfigurationList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Devices or create one.
    """

    schema = ConfigurationSchema
    # decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Configuration,
        "class": EsSqlalchemyDataLayer,
    }
