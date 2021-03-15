from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class DeviceCalibrationActionSchema(Schema):
    """
    This class create a schema for a device calibration action.
    It uses the  marshmallow-jsonapi library that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        type_ = "device_calibration_action"
        self_view = "api.device_calibration_action_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    current_calibration_date = fields.DateTime(required=True)
    next_calibration_date = fields.DateTime(allow_none=True)
    description = fields.Str(allow_none=True)
    formula = fields.Str(allow_none=True)
    value = fields.Float(allow_none=True)

    device = Relationship(
        attribute="device",
        self_view="api.device_calibration_action_device",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        include_resource_linkage=True,
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
        include_resource_linkage=True,
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

    device_property = Relationship(
        attribute="device_property",
        self_view="api.device_property_calibration_device_property",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<device_property_id>"},
        include_resource_linkage=True,
        schema="DevicePropertySchema",
        type_="device_property",
        id_field="id",
    )

    calibration_action = Relationship(
        attribute="calibration_action",
        self_view="api.device_property_calibration_calibration_action",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_property_calibration_detail",
        related_view_kwargs={"id": "<calibration_action_id>"},
        include_resource_linkage=True,
        schema="DeviceCalibrationActionSchema",
        type_="device_calibration_action",
        id_field="id",
    )
