from marshmallow import Schema as MarshmallowSchema
from marshmallow_jsonapi import fields


class AttachmentSchema(MarshmallowSchema):
    """
    This class create a schema for a attachment.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = 'attachment'

    id = fields.Integer(as_string=True, dump_only=True)
    label = fields.Str(allow_none=True)
    url = fields.Url(required=True)
