from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class PlatformMountActionSchema(Schema):
    """
    This class create a schema for a platform_mount_action.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        type_ = "platform_mount_action"
        self_view = "api.platform_mount_action_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    begin_date = fields.DateTime(required=True)
    description = fields.Str(allow_none=True)
    offset_x = fields.Float(allow_none=True)
    offset_y = fields.Float(allow_none=True)
    offset_z = fields.Float(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    platform = Relationship(
        attribute="platform",
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<platform_id>"},
        include_resource_linkage=True,
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    parent_platform = Relationship(
        attribute="parent_platform",
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<parent_platform_id>"},
        include_resource_linkage=True,
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    configuration = Relationship(
        attribute="configuration",
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        schema="ConfigurationSchema",
        type_="configuration",
        id_field="id",
    )
    contact = Relationship(
        attribute="contact",
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    created_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        id_field="id",
        dump_only=True,
    )
    updated_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        id_field="id",
        dump_only=True,
    )


class DeviceMountActionSchema(Schema):
    """
    This class create a schema for a device_mount_action.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        type_ = "device_mount_action"
        self_view = "api.device_mount_action_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    begin_date = fields.DateTime(required=True)
    description = fields.Str(allow_none=True)
    offset_x = fields.Float(allow_none=True)
    offset_y = fields.Float(allow_none=True)
    offset_z = fields.Float(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    device = Relationship(
        attribute="device",
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        include_resource_linkage=True,
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )
    parent_platform = Relationship(
        attribute="parent_platform",
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<parent_platform_id>"},
        include_resource_linkage=True,
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    configuration = Relationship(
        attribute="configuration",
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        schema="ConfigurationSchema",
        type_="configuration",
        id_field="id",
    )
    contact = Relationship(
        attribute="contact",
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    created_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        id_field="id",
        dump_only=True,
    )
    updated_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        id_field="id",
        dump_only=True,
    )
