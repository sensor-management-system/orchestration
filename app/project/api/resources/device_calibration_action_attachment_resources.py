from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from .base_resource import check_if_object_not_found
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

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceCalibrationAttachment not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

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
