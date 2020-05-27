from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema
from project.api.schemas.base_schema import \
    set_device_relationship_schema

class EventSchema(Schema):
    """
    This class create a schema for an event.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = 'event'
        self_view = 'events_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    description = fields.Str(required=True)
    date = fields.Date()

    device = set_device_relationship_schema('events')
