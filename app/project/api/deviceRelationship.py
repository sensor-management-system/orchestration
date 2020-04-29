from flask_rest_jsonapi import ResourceRelationship

from project.api.models.baseModel import db
from project.api.models.device import Device
from project.api.schemas.deviceSchema import DeviceSchema


class DeviceRelationship(ResourceRelationship):
    schema = DeviceSchema
    data_layer = {'session': db.session,
                  'model': Device}