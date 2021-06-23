from flask_rest_jsonapi import ResourceDetail

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
        add_updated_by_id(data)

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
    }
