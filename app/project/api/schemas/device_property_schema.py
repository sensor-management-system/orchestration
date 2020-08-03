from marshmallow import Schema as MarshmallowSchema
from marshmallow_jsonapi import fields


class DevicePropertySchema(MarshmallowSchema):
    """
    This class create a schema for a property.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = 'property'

    id = fields.Integer(as_string=True, dump_only=True)
    measuring_range_min = fields.Float(as_string=True, allow_none=True)
    measuring_range_max = fields.Float(as_string=True, allow_none=True)
    failure_value = fields.Float(as_string=True, allow_none=True)
    accuracy = fields.Str(allow_none=True)
    label = fields.Str(allow_none=True)
    unit_uri = fields.Str(allow_none=True)
    unit_name = fields.Str(allow_none=True)
    compartment_uri = fields.Str(allow_none=True)
    compartment_name = fields.Str(allow_none=True)
    property_uri = fields.Str(allow_none=True)
    property_name = fields.Str(allow_none=True)
    sampling_media_uri = fields.Str(allow_none=True)
    sampling_media_name = fields.Str(allow_none=True)
