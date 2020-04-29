from flask_rest_jsonapi import ResourceDetail
from project.api.schemas.deviceSchema import DeviceSchema
from project.api.models.device import Device

from project.api.models.baseModel import db

class DeviceDetail(ResourceDetail):
    schema = DeviceSchema
    data_layer = {'session': db.session,
                  'model': Device}