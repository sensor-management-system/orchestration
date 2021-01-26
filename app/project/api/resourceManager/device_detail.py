from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from project.api.flask_minio import FlaskMinio
from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.models.device_attachment import DeviceAttachment
from project.api.schemas.device_schema import DeviceSchema
from sqlalchemy.orm.exc import NoResultFound

from project.api import minio


def delete_attachments_in_minio_by_device_id(device_id_intended_for_deletion):
    """
    use the minio class to delete an attachment or a list of attachments
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

    def before_get_object(self, view_kwargs):
        if view_kwargs.get("id") is not None:
            try:
                _ = self.session.query(Device).filter_by(id=view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "device_id"},
                    "Device: {} not found".format(view_kwargs["id"]),
                )

    def before_delete(self, args, kwargs):
        """
        Delete the device attachments at the minio server
        :param args:
        :param kwargs:
        :return:
        """
        device_id_intended_for_deletion = kwargs.get("id")
        delete_attachments_in_minio_by_device_id(device_id_intended_for_deletion)
        return kwargs

    schema = DeviceSchema
    # decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
        "methods": {"before_get_object": before_get_object},
    }
