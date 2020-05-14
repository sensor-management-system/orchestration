from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class PlatformSchema(Schema):
    class Meta:
        type_ = 'platform'
        self_view = 'platform_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'platform_list'

    id = fields.Integer(as_string=True, dump_only=True)
    description = fields.Str(allow_none=True)
    short_name = fields.Str(required=True)
    long_name = fields.Str(allow_none=True)
    manufacturer = fields.Str(allow_none=True)
    type = fields.Str(required=True)
    platform_type = fields.Str(allow_none=True)
    src = fields.Str(allow_none=True)
    configuration_date = fields.Date(allow_none=True)
    inventory_number = fields.Integer(allow_none=True)
    urn = fields.Function(lambda obj: "{}_{}".format(
        obj.type.upper(), obj.short_name.upper()))
    devices = Relationship(self_view='platform_devices',
                           self_view_kwargs={'id': '<id>'},
                           related_view='devices_list',
                           related_view_kwargs={'id': '<id>'},
                           many=True,
                           schema='DeviceSchema',
                           type_='device')

    contacts = Relationship(attribute='contacts',
                            self_view='platform_contacts',
                            self_view_kwargs={'id': '<id>'},
                            related_view='contacts_list',
                            related_view_kwargs={'platform_id': '<id>'},
                            many=True,
                            schema='ContactSchema',
                            type_='contact',
                            id_field='contact_id')
