from flask import request
from flask_rest_jsonapi import ResourceRelationship

from ..auth.permission_utils import is_user_in_a_group, check_parent_group_before_change_a_relationship
from ..helpers.errors import ForbiddenError
from ..models.base_model import db
from ..models.device import Device
from ..schemas.device_schema import DeviceSchema
from ..token_checker import token_required


class DeviceRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Device and objects.
    """

    def before_post(self, args, kwargs, json_data=None):
        check_parent_group_before_change_a_relationship(f"devices/", self._data_layer.model)

    def before_patch(self, args, kwargs, json_data=None):
        check_parent_group_before_change_a_relationship("device/", self._data_layer.model)

    def before_delete(self, args, kwargs, json_data=None):
        check_parent_group_before_change_a_relationship(f"devices/", self._data_layer.model)

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": Device}
