from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


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

    device = Relationship(attribute='device',
                          self_view='device_contacts',
                          self_view_kwargs={'id': '<id>'},
                          related_view='devices_detail',
                          related_view_kwargs={'id': '<id>'},
                          schema='DeviceSchema',
                          type_='device')

    platform = Relationship(attribute='platform',
                            self_view='platform_contacts',
                            self_view_kwargs={'id': '<id>'},
                            related_view='platform_detail',
                            related_view_kwargs={'id': '<id>'},
                            schema='PlatformSchema',
                            type_='platform')
