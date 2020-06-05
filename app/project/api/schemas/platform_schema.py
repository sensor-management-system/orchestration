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
    manufacturer_uri = fields.Str(allow_none=True)
    manufacturer_name = fields.Str(allow_none=True)
    model = fields.Str(required=True)
    platform_type_uri = fields.Str(allow_none=True)
    platform_type_name = fields.Str(allow_none=True)
    status_uri = fields.Str(allow_none=True)
    status_name = fields.Str(allow_none=True)
    website = fields.Url(allow_none=True)
    created_at = fields.Date(allow_none=True)
    modified_at = fields.Date(allow_none=True)
    created_by = fields.Date(allow_none=True)
    created_by_id = fields.Date(allow_none=True)
    modified_by = fields.Date(allow_none=True)
    modified_by_id = fields.Date(allow_none=True)
    inventory_number = fields.Str(allow_none=True)
    serial_number = fields.Str(allow_none=True)
    persistent_identifier = fields.Str(allow_none=True)
    contacts = Relationship(attribute='contacts',
                            self_view='platforms_contacts',
                            self_view_kwargs={'id': '<id>'},
                            related_view='contacts_list',
                            related_view_kwargs={'platform_id': '<id>'},
                            many=True,
                            schema='ContactSchema',
                            type_='contact',
                            id_field='id'
                            )
