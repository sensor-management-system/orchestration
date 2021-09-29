from flask_rest_jsonapi import ResourceDetail, JsonApiException
from flask_rest_jsonapi.exceptions import ObjectNotFound

from .base_resource import delete_attachments_in_minio_by_url
from ..helpers.errors import ConflictError
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

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        device = db.session.query(Device).filter_by(id=kwargs["id"]).first()
        if device is None:
            raise ObjectNotFound({"pointer": ""}, "Object Not Found")
        urls = [a.url for a in device.device_attachments]
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError("Deletion failed for the device.", str(e))

        for url in urls:
            delete_attachments_in_minio_by_url(url)

        final_result = {"meta": {"message": "Object successfully deleted"}}
        return final_result

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
    }
