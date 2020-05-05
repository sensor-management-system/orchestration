from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


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
    src = fields.Str(required=True)

    device = Relationship(attribute='device',
                          self_view='device_attachments',
                          self_view_kwargs={'id': '<id>'},
                          related_view='devices_detail',
                          related_view_kwargs={'id': '<id>'},
                          schema='DeviceSchema',
                          type_='device')
