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
        self_view = 'user_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    subject = fields.Str(required=True)

    contact = Relationship(attribute='contact',
                           self_view='contact_user',
                           self_view_kwargs={'id': '<id>'},
                           related_view='contact_detail',
                           related_view_kwargs={'id': '<id>'},
                           include_resource_linkage=True,
                           schema='ContactSchema',
                           type_='contact',
                           id_field='id'
                           )
