"""Module for the device property relationship resource."""
from flask_rest_jsonapi import ResourceRelationship

from ..models.base_model import db
from ..models.device_property import DeviceProperty
from ..schemas.device_property_schema import DevicePropertySchema
from ..token_checker import token_required


class DevicePropertyRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Device and objects.
    """

    schema = DevicePropertySchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceProperty}
