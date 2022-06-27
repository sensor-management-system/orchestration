"""Module for the platform schema."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from ..schemas.attachment_schema import AttachmentSchema
from ..schemas.contact_schema import ContactSchema


class PlatformSchema(Schema):
    """
    Schema to serialize platform model instances.

    Intended to work with a JSON:API.
    """

    class Meta:
        """Meta class for PlatformSchema class."""

        type_ = "platform"
        self_view = "api.platform_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.platform_list"

    id = fields.Integer(as_string=True)
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
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    group_ids = fields.Field(many=True, allow_none=True)
    is_private = fields.Boolean(allow_none=True)
    is_internal = fields.Boolean(allow_none=True)
    is_public = fields.Boolean(allow_none=True)
    created_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        dump_only=True,
    )
    updated_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        dump_only=True,
    )
    inventory_number = fields.Str(allow_none=True)
    serial_number = fields.Str(allow_none=True)
    persistent_identifier = fields.Str(allow_none=True)
    platform_attachments = Relationship(
        related_view="api.platform_attachment_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="PlatformAttachmentSchema",
        type_="platform_attachment",
        id_field="id",
    )
    contacts = Relationship(
        related_view="api.contact_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    generic_platform_actions = Relationship(
        related_view="api.generic_platform_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="GenericPlatformActionSchema",
        type_="generic_platform_action",
        id_field="id",
    )
    platform_mount_actions = Relationship(
        related_view="api.platform_mount_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="PlatformMountActionSchema",
        type_="platform_mount_actions",
        id_field="id",
    )
    platform_software_update_actions = Relationship(
        related_view="api.platform_software_update_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="PlatformSoftwareUpdateActionSchema",
        type_="platform_software_update_action",
        id_field="id",
    )
    outer_platform_mount_actions = Relationship(
        related_view="api.platform_mount_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="PlatformMountActionSchema",
        type_="platform_mount_actions",
        id_field="id",
    )
    outer_device_mount_actions = Relationship(
        related_view="api.device_mount_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="DeviceMountActionSchema",
        type_="device_mount_action",
        id_field="id",
    )

    @staticmethod
    def nested_dict_serializer(obj):
        """Serialize the object to a nested dict."""
        return PlatformToNestedDictSerializer().to_nested_dict(obj)


class PlatformToNestedDictSerializer:
    """
    Serializer to create nested dicts from platforms.

    While the "normal" serializer is used for the JSON:API, this
    here can be used to just create a nested dict of the content of
    a platform.

    This can then be flattened and used for example for a csv export.
    """

    @staticmethod
    def to_nested_dict(platform):
        """
        Convert to nested dict.

        :param platform:
        :return:
        """
        if platform is not None:
            return {
                "short_name": platform.short_name,
                "long_name": platform.long_name,
                "description": platform.description,
                "manufacturer_name": platform.manufacturer_name,
                "manufacturer_uri": platform.manufacturer_uri,
                "model": platform.model,
                "platform_type_name": platform.platform_type_name,
                "status_name": platform.status_name,
                "website": platform.website,
                "inventory_number": platform.inventory_number,
                "serial_number": platform.serial_number,
                "persistent_identifier": platform.persistent_identifier,
                "attachments": [
                    AttachmentSchema().dict_serializer(a)
                    for a in platform.platform_attachments
                ],
                "contacts": [
                    ContactSchema().dict_serializer(c) for c in platform.contacts
                ],
            }


class PlatformSchemaForOnlyId(Schema):
    class Meta:

        type_ = "platform"
        self_view = "api.platform_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.platform_list"

    id = fields.Integer(as_string=True)
