from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class PlatformMountActionSchema(Schema):
    class Meta:
        type_ = "platform_mount_action"
        self_view = "api.platform_mount_action_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    begin_date = fields.DateTime(allow_none=False)
    description = fields.Str(allow_none=True)
    offset_x = fields.Float(allow_none=True)
    offset_y = fields.Float(allow_none=True)
    offset_z = fields.Float(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    platform = Relationship(
        attribute="platform",
        self_view="api.platform_mount_action_platform",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<platform_id>"},
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    parent_platform = Relationship(
        attribute="parent_platform",
        self_view="api.platform_mount_action_parent_platform",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<parent_platform_id>"},
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    configuration = Relationship(
        attribute="configuration",
        self_view="api.platform_mount_action_configuration",
        self_view_kwargs={"id": "<id>"},
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        schema="ConfigurationSchema",
        type_="configuration",
        id_field="id",
    )
    contact = Relationship(
        attribute="contact",
        self_view="api.platform_mount_action_contact",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<id>"},
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    created_by = Relationship(
        self_view="api.platform_mount_action_created_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        type_="user",
        id_field="id",
    )
    updated_by = Relationship(
        self_view="api.platform_mount_action_updated_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        type_="user",
        id_field="id",
    )


class DeviceMountActionSchema(Schema):
    class Meta:
        type_ = "device_mount_action"
        self_view = "api.device_mount_action_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    begin_date = fields.DateTime(allow_none=False)
    description = fields.Str(allow_none=True)
    offset_x = fields.Float(allow_none=True)
    offset_y = fields.Float(allow_none=True)
    offset_z = fields.Float(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    device = Relationship(
        attribute="device",
        self_view="api.mount_device_action_device",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )
    parent_platform = Relationship(
        attribute="parent_platform",
        self_view="api.mount_device_action_parent_platform",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<parent_platform_id>"},
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    configuration = Relationship(
        attribute="configuration",
        self_view="api.mount_device_action_configuration",
        self_view_kwargs={"id": "<id>"},
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        schema="ConfigurationSchema",
        type_="configuration",
        id_field="id",
    )
    contact = Relationship(
        attribute="contact",
        self_view="api.mount_device_action_contact",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<id>"},
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    created_by = Relationship(
        self_view="api.device_mount_action_created_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        type_="user",
        id_field="id",
    )
    updated_by = Relationship(
        self_view="api.device_mount_action_updated_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        type_="user",
        id_field="id",
    )
