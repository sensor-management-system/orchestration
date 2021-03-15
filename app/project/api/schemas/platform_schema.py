"""Module for the platform schema."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from project.api.schemas.attachment_schema import AttachmentSchema
from project.api.schemas.contact_schema import ContactSchema


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
    created_by = Relationship(
        self_view="api.platform_created_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
    )
    updated_by = Relationship(
        self_view="api.platform_updated_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
    )
    inventory_number = fields.Str(allow_none=True)
    serial_number = fields.Str(allow_none=True)
    persistent_identifier = fields.Str(allow_none=True)
    platform_attachments = Relationship(
        related_view="api.platform_platform_attachments",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="PlatformAttachmentSchema",
        type_="platform_attachment",
        id_field="id",
    )
    contacts = Relationship(
        related_view="api.platform_contacts",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    generic_platform_actions = Relationship(
        related_view="api.platform_generic_platform_actions",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="GenericPlatformActionSchema",
        type_="generic_platform_action",
        id_field="id",
    )
    platform_mount_actions = Relationship(
        related_view="api.platform_platform_mount_actions",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="PlatformMountActionSchema",
        type_="platform_mount_actions",
        id_field="id",
    )
    platform_unmount_actions = Relationship(
        related_view="api.platform_platform_unmount_actions",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="PlatformUnmountActionSchema",
        type_="platform_unmount_actions",
        id_field="id",
    )
    platform_software_update_actions = Relationship(
        related_view="api.platform_platform_software_update_actions",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="PlatformSoftwareUpdateActionAttachmentSchema",
        type_="platform_software_update_action_attachment",
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
