from flask_rest_jsonapi import ResourceDetail

from ..helpers.errors import ForbiddenError
from ..helpers.permission import is_user_in_a_group, is_user_Admin_in_a_group
from ..models.base_model import db
from ..models.device import Device
from ..resourceManager.base_resource import add_updated_by_id
from ..schemas.device_schema import DeviceSchema
from ..token_checker import token_required


class DeviceDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data"""
        groups_ids = db.session.query(Device).filter_by(id=data['id']).first().groups_ids
        if is_user_in_a_group(groups_ids):
            add_updated_by_id(data)
        else:
            raise ForbiddenError(f"User should be in this groups:{groups_ids}")

    def before_delete(self, args, kwargs):
        groups_ids = db.session.query(Device).filter_by(id=kwargs['id']).first().groups_ids
        if not is_user_Admin_in_a_group(groups_ids):
            raise ForbiddenError(f"User should be admin in one of this groups:{groups_ids}")

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
    }
