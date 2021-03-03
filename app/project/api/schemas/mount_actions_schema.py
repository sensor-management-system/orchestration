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
    platform = Relationship(
        attribute="platforms",
        self_view="api.platform_mount_action_platform",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<id>"},
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    parent_platform = Relationship(
        attribute="parent_platform",
        self_view="api.platform_mount_action_parent_platform",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<id>"},
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    configuration = Relationship(
        attribute="configurations",
        self_view="api.platform_mount_action_configuration",
        self_view_kwargs={"id": "<id>"},
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<id>"},
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
    device = Relationship(
        attribute="device",
        self_view="api.mount_device_action_device",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_detail",
        related_view_kwargs={"id": "<id>"},
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )
    parent_platform = Relationship(
        attribute="parent_platform",
        self_view="api.mount_device_action_parent_platform",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<id>"},
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    configuration = Relationship(
        attribute="configuration",
        self_view="api.mount_device_action_configuration",
        self_view_kwargs={"id": "<id>"},
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<id>"},
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
