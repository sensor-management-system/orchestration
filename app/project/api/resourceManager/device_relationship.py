from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.schemas.device_schema import DeviceSchema
from project.api.token_checker import token_required


class DeviceRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Device and objects.
    """

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": Device}
