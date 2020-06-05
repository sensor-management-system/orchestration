from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class UserSchema(Schema):
    """
    This class create a schema for a user.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = 'user'
        self_view = 'users_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    user_name = fields.Str(allow_none=True)
    value = fields.Str(allow_none=True)

    contact = Relationship(attribute='contact',
                           self_view='contact_user',
                           self_view_kwargs={'id': '<id>'},
                           related_view='contacts_detail',
                           related_view_kwargs={'id': '<id>'},
                           include_resource_linkage=True,
                           schema='ContactSchema',
                           type_='contact',
                           id_field='id'
                           )

    events = Relationship(attribute='events',
                          self_view='user_events',
                          self_view_kwargs={'id': '<id>'},
                          related_view='events_list',
                          related_view_kwargs={'user_id': '<id>'},
                          many=True,
                          include_resource_linkage=True,
                          schema='EventSchema',
                          type_='event',
                          id_field='id'
                          )
