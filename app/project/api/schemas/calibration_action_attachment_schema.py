from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class DeviceCalibrationAttachmentSchema(Schema):
    class Meta:
        type_ = "device_calibration_attachment"
        self_view = "api.device_calibration_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.device_calibration_attachment_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        self_view="api.device_calibration_attachment_action",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_calibration_action_detail",
        related_view_kwargs={"id": "<id>"},
        schema="DeviceCalibrationActionSchema",
        type="device_calibration_action",
        id_field="id",
    )
    attachment = Relationship(
        self_view="api.device_calibration_attachment_attachment",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_calibration_attachment_detail",
        related_view_kwargs={"id": "<id>"},
        schema="DeviceAttachmentSchema",
        type_="device_attachment",
        id_field="id",
    )
