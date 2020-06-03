from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.schemas.device_schema import DeviceSchema


class DeviceRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Device and objects.
    """
    schema = DeviceSchema
    data_layer = {'session': db.session,
                  'model': Device}
