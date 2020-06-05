from flask_rest_jsonapi import ResourceList
from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.schemas.device_schema import DeviceSchema


class DeviceList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Devices or create one.
    """

    schema = DeviceSchema
    data_layer = {'session': db.session,
                  'model': Device}
