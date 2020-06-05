from marshmallow import Schema as MarshmallowSchema
from marshmallow_jsonapi import fields


class CustomFieldSchema(MarshmallowSchema):
    """
    This class create a schema for a custom field.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = 'customfield'

    id = fields.Integer(as_string=True, dump_only=True)
    key = fields.Str(allow_none=True)
    value = fields.Str(allow_none=True)
