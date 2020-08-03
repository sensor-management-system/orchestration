from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship
from project.api.schemas.attachment_schema import AttachmentSchema


class PlatformSchema(Schema):
    class Meta:
        type_ = 'platform'
        self_view = 'platform_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'platform_list'

    id = fields.Integer(as_string=True, dump_only=True)
    description = fields.Str(allow_none=True)
    short_name = fields.Str(required=True, data_key="shortName")
    long_name = fields.Str(allow_none=True, data_key="longName")
    manufacturer_uri = fields.Str(allow_none=True, data_key="manufacturerUri"
    manufacturer_name = fields.Str(allow_none=True, data_key="manufacturerName")
    model = fields.Str(allow_none=True)
    platform_type_uri = fields.Str(allow_none=True, data_key="platformTypeUri")
    platform_type_name = fields.Str(allow_none=True, data_key="platformTypeName")
    status_uri = fields.Str(allow_none=True, data_key="statusUri")
    status_name = fields.Str(allow_none=True, data_key="statusName")
    website = fields.Url(allow_none=True)
    created_at = fields.DateTime(allow_none=True, data_key="createdAt")
    modified_at = fields.DateTime(allow_none=True, data_key="modifiedAt")
    #created_by = fields.Date(allow_none=True)
    created_by_id = fields.Integer(allow_none=True, dump_only=True, data_key="createdById")
    #modified_by = fields.Date(allow_none=True)
    modified_by_id = fields.Integer(allow_none=True, data_key="modifiedById")
    inventory_number = fields.Str(allow_none=True, data_key="intentoryNumber")
    serial_number = fields.Str(allow_none=True, data_key="serialNumber")
    persistent_identifier = fields.Str(allow_none=True, data_key="persistentIdentifier")
    platform_attachments = fields.Nested(AttachmentSchema, many=True, allow_none=True, data_key="attachments")
    contacts = Relationship(attribute='contacts',
                            self_view='platform_contacts',
                            self_view_kwargs={'id': '<id>'},
                            related_view='contact_list',
                            related_view_kwargs={'platform_id': '<id>'},
                            many=True,
                            schema='ContactSchema',
                            type_='contact',
                            id_field='id'
                            )
