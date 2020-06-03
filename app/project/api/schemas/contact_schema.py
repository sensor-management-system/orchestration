from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema
from project.api.schemas.base_schema import \
    set_device_relationship_schema, set_platform_relationship_schema


class ContactSchema(Schema):
    """
    This class create a schema for a contact.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = 'contact'
        self_view = 'contacts_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    username = fields.Str(allow_none=True)
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    email = fields.Str(required=True)

    device = set_device_relationship_schema('contacts')

    platform = set_platform_relationship_schema('contacts')
