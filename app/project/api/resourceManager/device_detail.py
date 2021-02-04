from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.resourceManager.base_resource import add_updated_by_id
from project.api.schemas.device_schema import DeviceSchema
from project.api.models.device_attachment import DeviceAttachment
from project.api.token_checker import token_required

from project.api import minio


def delete_attachments_in_minio_by_device_id(device_id_intended_for_deletion):
    """
    Use the minio class to delete an attachment or a list of attachments.
    :param device_id_intended_for_deletion:
    :return:
    """
    attachments_related_to_device = (
        db.session.query(DeviceAttachment)
            .filter_by(device_id=device_id_intended_for_deletion)
            .all()
    )
    for attachment in attachments_related_to_device:
        minio.remove_an_object(attachment.url)


class DeviceDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data"""
        add_updated_by_id(data)

    def before_delete(self, args, kwargs):
        """
        Delete the device attachments at the minio server.
        :param args:
        :param kwargs:
        :return:
        """
        device_id_intended_for_deletion = kwargs.get("id")
        delete_attachments_in_minio_by_device_id(device_id_intended_for_deletion)
        return kwargs

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
    }
