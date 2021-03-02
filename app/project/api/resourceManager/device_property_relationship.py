"""Module for the device property relationship resource."""
from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.device_property import DeviceProperty
from project.api.schemas.device_property_schema import DevicePropertySchema
from project.api.token_checker import token_required


class DevicePropertyRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Device and objects.
    """

    schema = DevicePropertySchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceProperty}
