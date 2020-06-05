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
    given_name = fields.Str(allow_none=True)
    family_name = fields.Str(allow_none=True)
    website = fields.Str(allow_none=True)
    email = fields.Str(required=True)

    platforms = Relationship(attribute='platforms',
                             self_view='contacts_platforms',
                             self_view_kwargs={'id': '<id>'},
                             related_view='platform_list',
                             related_view_kwargs={'contact_id': '<id>'},
                             many=True,
                             schema='PlatformSchema',
                             type_='platform',
                             id_field='id'
                             )
    devices = Relationship(attribute='devices',
                           self_view='contacts_devices',
                           self_view_kwargs={'id': '<id>'},
                           related_view='devices_list',
                           related_view_kwargs={'contact_id': '<id>'},
                           many=True,
                           schema='DeviceSchema',
                           type_='device',
                           id_field='id'
                           )
    user = Relationship(self_view='contact_user',
                        self_view_kwargs={'id': '<id>'},
                        related_view='users_list',
                        related_view_kwargs={'id': '<id>'},
                        many=True,
                        include_resource_linkage=True,
                        schema='UserSchema',
                        type_='user',
                        id_field='id'
                        )
