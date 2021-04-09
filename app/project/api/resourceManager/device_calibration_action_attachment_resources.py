from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from .base_resource import delete_attachments_in_minio_by_id
from ..models.base_model import db
from ..models.calibration_attachments import DeviceCalibrationAttachment
from ..schemas.calibration_action_attachment_schema import (
    DeviceCalibrationAttachmentSchema,
)
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class DeviceCalibrationAttachmentList(ResourceList):
    """
    List resource for device calibration attachment.
    """

    schema = DeviceCalibrationAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceCalibrationAttachment}


class DeviceCalibrationAttachmentDetail(ResourceDetail):
    """
    Detail resource for device calibration attachment.
    """

    def before_delete(self, args, kwargs):
        """Hook to delete attachment from storage server before delete method"""
        delete_attachments_in_minio_by_id(DeviceCalibrationAttachment, kwargs["id"])

    schema = DeviceCalibrationAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceCalibrationAttachment}


class DeviceCalibrationAttachmentRelationship(ResourceRelationship):
    """
    Relationship resource for device calibration attachment.
    """

    schema = DeviceCalibrationAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceCalibrationAttachment}
