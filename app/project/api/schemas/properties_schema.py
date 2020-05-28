from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema
from project.api.schemas.base_schema import \
    set_device_relationship_schema


class PropertiesSchema(Schema):
    """
    This class create a schema for a properties.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = 'properties'
        self_view = 'properties_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    accuracy = fields.Str(allow_none=True)
    label = fields.Str(allow_none=True)
    unit = fields.Str(allow_none=True)
    Compartment = fields.Str(allow_none=True)
    measuring_range_min = fields.Float(as_string=True, allow_none=True)
    measuring_range_max = fields.Float(as_string=True, allow_none=True)
    failure_value = fields.Float(as_string=True, allow_none=True)
    Variable = fields.Str(allow_none=True)
    sampling_media = fields.Str(allow_none=True)

    device = set_device_relationship_schema('properties')
