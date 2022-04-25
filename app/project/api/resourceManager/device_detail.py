from flask_rest_jsonapi import JsonApiException, ResourceDetail

from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_updated_by_id
from ..models.base_model import db
from ..models.device import Device
from ..schemas.device_schema import DeviceSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found, delete_attachments_in_minio_by_url


class DeviceDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        device = check_if_object_not_found(Device, kwargs)
        urls = [a.url for a in device.device_attachments]
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError("Deletion failed for the device.", str(e))

        for url in urls:
            delete_attachments_in_minio_by_url(url)

        final_result = {"meta": {"message": "Object successfully deleted"}}
        return final_result

    def before_patch(self, args, kwargs, data):
        """
        Run logic before the patch.

        In this case we want to make sure that we update the updated_by_id
        with the id of the user that run the request.
        """
        add_updated_by_id(data)

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
    }
