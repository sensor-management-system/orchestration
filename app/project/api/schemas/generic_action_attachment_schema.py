from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class GenericDeviceActionAttachmentSchema(Schema):
    class Meta:
        type_ = "generic_device_action_attachment"
        self_view = "api.generic_device_action_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.generic_device_action_attachment_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        self_view="api.generic_device_action_attachment_action",
        self_view_kwargs={"id": "<id>"},
        related_view="api.generic_device_action_detail",
        related_view_kwargs={"id": "<id>"},
        schema="GenericDeviceActionSchema",
        type="generic_device_action",
        id_field="id",
    )
    attachment = Relationship(
        self_view="api.generic_device_action_attachment_attachment",
        self_view_kwargs={"id": "<id>"},
        related_view="api.generic_device_action_attachment_detail",
        related_view_kwargs={"id": "<attachment_id>"},
        schema="DeviceAttachment",
        type_="device_attachment",
        id_field="id",
    )


class GenericPlatformActionAttachmentSchema(Schema):
    class Meta:
        type_ = "generic_platform_action_attachment"
        self_view = "api.generic_platform_action_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.generic_platform_action_attachment_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        self_view="api.generic_platform_action_attachment_action",
        self_view_kwargs={"id": "<id>"},
        related_view="api.generic_platform_action_detail",
        related_view_kwargs={"id": "<id>"},
        schema="GenericPlatformActionSchema",
        type="generic_platform_action",
        id_field="id",
    )
    attachment = Relationship(
        self_view="api.generic_platform_action_attachment_attachment",
        self_view_kwargs={"id": "<id>"},
        related_view="api.generic_platform_action_attachment_detail",
        related_view_kwargs={"id": "<id>"},
        schema="PlatformAttachmentSchema",
        type_="platform_attachment",
        id_field="id",
    )


class GenericConfigurationActionAttachmentSchema(Schema):
    class Meta:
        type_ = "generic_configuration_action_attachment_schema"
        self_view = "api.generic_configuration_action_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.generic_configuration_action_attachment_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        self_view="api.generic_configuration_action_attachment_action",
        self_view_kwargs={"id": "<id>"},
        related_view="api.generic_configuration_action_detail",
        related_view_kwargs={"id": "<id>"},
        schema="GenericConfigurationActionSchema",
        type="generic_configuration_action",
        id_field="id",
    )
    attachment = Relationship(
        self_view="api.generic_configuration_action_attachment_attachment",
        self_view_kwargs={"id": "<id>"},
        related_view="api.generic_configuration_action_attachment_detail",
        related_view_kwargs={"id": "<id>"},
        schema="ConfigurationAttachmentSchema",
        type_="configuration_attachment",
        id_field="id",
    )
