from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema
from project.api.schemas.base_schema import \
    set_device_relationship_schema


class AttachmentSchema(Schema):
    """
    This class create a schema for a attachment.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = 'attachment'
        self_view = 'attachments_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    label = fields.Str(allow_none=True)
    url = fields.Str(required=True)
    device = set_device_relationship_schema('attachments')
