from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class DeviceCalibrationActionSchema(Schema):
    class Meta:
        type_ = "device_calibration_action"
        self_view = "api.device_calibration_action_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    current_calibration_date = fields.DateTime(allow_none=False)
    next_calibration_date = fields.DateTime(allow_none=True)
    description = fields.Str(allow_none=True)
    formula = fields.Str(allow_none=True)
    value = fields.Float(allow_none=True)

    device = Relationship(
        attribute="device",
        self_view="api.device_calibration_action_platform",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )
    contact = Relationship(
        attribute="contact",
        self_view="api.device_calibration_action_contact",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )


class DevicePropertyCalibrationSchema(Schema):
    class Meta:
        type_ = "device_property_calibration"
        self_view = "api.device_property_calibration_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)

    device = Relationship(
        attribute="device",
        self_view="api.mount_device_action_device",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_detail",
        related_view_kwargs={"id": "<id>"},
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )

    calibration_action = Relationship(
        attribute="device_calibration_action",
        self_view="api.mount_device_action_calibration_action",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_calibration_action_detail",
        related_view_kwargs={"id": "<device_calibration_action_id>"},
        schema="DeviceCalibrationActionSchema",
        type_="device_calibration_action",
        id_field="id",
    )
