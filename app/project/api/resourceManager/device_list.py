from flask_rest_jsonapi import ResourceList
from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.schemas.device_schema import DeviceSchema
from project.api.data_layers.esalchemy import EsSqlalchemyDataLayer
from project.api.token_checker import token_required


class DeviceList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Devices or create one.
    """

    schema = DeviceSchema
    # decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
        "class": EsSqlalchemyDataLayer,
    }
