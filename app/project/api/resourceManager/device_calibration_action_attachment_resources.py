from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.calibration_attachments import DeviceCalibrationAttachment
from project.api.schemas.calibration_action_attachment_schema import (
    DeviceCalibrationAttachmentSchema,
)
from project.frj_csv_export.resource import ResourceList


class DeviceCalibrationAttachmentList(ResourceList):
    schema = DeviceCalibrationAttachmentSchema
    data_layer = {"session": db.session, "model": DeviceCalibrationAttachment}


class DeviceCalibrationAttachmentDetail(ResourceDetail):
    schema = DeviceCalibrationAttachmentSchema
    data_layer = {"session": db.session, "model": DeviceCalibrationAttachment}


class DeviceCalibrationAttachmentRelationship(ResourceRelationship):
    schema = DeviceCalibrationAttachmentSchema
    data_layer = {"session": db.session, "model": DeviceCalibrationAttachment}
