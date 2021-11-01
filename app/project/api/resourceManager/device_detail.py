from flask_rest_jsonapi import ResourceDetail, JsonApiException
from flask_rest_jsonapi.exceptions import ObjectNotFound

from .base_resource import delete_attachments_in_minio_by_url
from ..helpers.errors import ConflictError
from ..helpers.permission_helpers import (
    check_for_permissions,
    check_patch_permission,
    check_deletion_permission,
)
from ..models.base_model import db
from ..models.device import Device
from ..schemas.device_schema import DeviceSchema
from ..token_checker import token_required


class DeviceDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    def before_get(self, args, kwargs):
        """Check user permission to view a Device."""
        check_for_permissions(Device, kwargs)

    def before_patch(self, args, kwargs, data):
        """Checks for permission"""
        check_patch_permission(data, Device)

    def before_delete(self, args, kwargs):
        """Checks for permission"""
        check_deletion_permission(kwargs, Device)

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
