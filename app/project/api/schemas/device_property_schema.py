from marshmallow import Schema as MarshmallowSchema
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class InnerDevicePropertySchema(MarshmallowSchema):
    """
    This is the very same class as DevicePropertySchema,
    but it uses just a normal marshmallow schema in order
    to support its usage as a nested element within the
    devices schema.
    """

    class Meta:
        type_ = "property"

    id = fields.Integer(as_string=True)
    measuring_range_min = fields.Float(allow_none=True)
    measuring_range_max = fields.Float(allow_none=True)
    failure_value = fields.Float(allow_none=True)
    accuracy = fields.Float(allow_none=True)
    label = fields.Str(allow_none=True)
    unit_uri = fields.Str(allow_none=True)
    unit_name = fields.Str(allow_none=True)
    compartment_uri = fields.Str(allow_none=True)
    compartment_name = fields.Str(allow_none=True)
    property_uri = fields.Str(allow_none=True)
    property_name = fields.Str(allow_none=True)
    sampling_media_uri = fields.Str(allow_none=True)
    sampling_media_name = fields.Str(allow_none=True)
    resolution = fields.Float(allow_none=True)
    resolution_unit_uri = fields.String(allow_none=True)
    resolution_unit_name = fields.String(allow_none=True)


class DevicePropertySchema(Schema):
    """
    This class create a schema for a property.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = "device_property"
        self_view = "device_property_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True, )
    measuring_range_min = fields.Float(allow_none=True)
    measuring_range_max = fields.Float(allow_none=True)
    failure_value = fields.Float(allow_none=True)
    accuracy = fields.Float(allow_none=True)
    label = fields.Str(allow_none=True)
    unit_uri = fields.Str(allow_none=True)
    unit_name = fields.Str(allow_none=True)
    compartment_uri = fields.Str(allow_none=True)
    compartment_name = fields.Str(allow_none=True)
    property_uri = fields.Str(allow_none=True)
    property_name = fields.Str(allow_none=True)
    sampling_media_uri = fields.Str(allow_none=True)
    sampling_media_name = fields.Str(allow_none=True)

    device = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="device_detail",
        related_view_kwargs={"id": "<device_id>"},
        type_="device",
    )
