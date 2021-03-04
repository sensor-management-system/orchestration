from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class DeviceCalibrationAttachmentSchema(Schema):
    class Meta:
        type_ = "device_calibration_action_schema"
        self_view = "api.device_calibration_action_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.device_calibration_action_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        self_view="api.device_calibration_action_action",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_calibration_action_detail",
        related_view_kwargs={"id": "<action_id>"},
        schema="GenericDeviceActionSchema",
        type="device_calibration_action",
        id_field="id",
    )
    attachment = Relationship(
        self_view="api.device_calibration_action_attachment",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_calibration_action_detail",
        related_view_kwargs={"action_id": "<id>"},
        schema="DeviceCalibrationAttachmentSchema",
        type_="device_calibration_action",
        id_field="id",
    )
