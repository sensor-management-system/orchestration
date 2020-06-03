from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.schemas.device_schema import DeviceSchema


class DeviceDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete a Device
    """
    schema = DeviceSchema
    data_layer = {'session': db.session,
                  'model': Device}
