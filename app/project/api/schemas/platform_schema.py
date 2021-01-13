from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship
from project.api.schemas.attachment_schema import AttachmentSchema


class PlatformSchema(Schema):
    class Meta:
        type_ = "platform"
        self_view = "api.platform_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.platform_list"

    id = fields.Integer(as_string=True, )
    description = fields.Str(allow_none=True)
    short_name = fields.Str(required=True)
    long_name = fields.Str(allow_none=True)
    manufacturer_uri = fields.Str(allow_none=True)
    manufacturer_name = fields.Str(allow_none=True)
    model = fields.Str(allow_none=True)
    platform_type_uri = fields.Str(allow_none=True)
    platform_type_name = fields.Str(allow_none=True)
    status_uri = fields.Str(allow_none=True)
    status_name = fields.Str(allow_none=True)
    website = fields.Str(allow_none=True)
    created_at = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(allow_none=True)
    created_by = Relationship(
        self_view="api.platform_created_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        type_="user",
    )
    updated_by = Relationship(
        self_view="api.platform_updated_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        type_="user",
    )
    inventory_number = fields.Str(allow_none=True)
    serial_number = fields.Str(allow_none=True)
    persistent_identifier = fields.Str(allow_none=True)
    attachments = fields.Nested(
        AttachmentSchema, many=True, allow_none=True, attribute="platform_attachments"
    )
    contacts = Relationship(
        attribute="contacts",
        self_view="api.platform_contacts",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_list",
        related_view_kwargs={"platform_id": "<id>"},
        many=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
