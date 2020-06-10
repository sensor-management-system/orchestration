from marshmallow import Schema as MarshmallowSchema
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship


class EventSchema(MarshmallowSchema):
    """
    This class create a schema for an event.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = 'event'

    id = fields.Integer(as_string=True, dump_only=True)
    description = fields.Str(required=True)
    date = fields.Date()
    user = Relationship(self_view='events_user',
                        self_view_kwargs={'id': '<id>'},
                        related_view='events_list',
                        related_view_kwargs={'id': '<id>'},
                        many=True,
                        include_resource_linkage=True,
                        schema='UserSchema',
                        type_='user',
                        id_field='id'
                        )
