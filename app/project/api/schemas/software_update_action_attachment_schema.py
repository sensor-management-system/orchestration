from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class DeviceSoftwareUpdateActionAttachmentSchema(Schema):
    class Meta:
        type_ = "device_software_update_action_attachment"
        self_view = "api.device_software_update_action_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.device_software_update_action_attachment_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        self_view="api.device_software_update_action_attachment_action",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_software_update_action_attachment_detail",
        related_view_kwargs={"id": "<id>"},
        schema="DeviceSoftwareUpdateActionSchema",
        type_="device_software_update_action",
        id_field="id",
    )
    attachment = Relationship(
        self_view="api.device_software_update_action_attachment_attachment",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_attachment_detail",
        related_view_kwargs={"id": "<id>"},
        schema="DeviceAttachmentSchema",
        type_="device_attachment",
        id_field="id",
    )


class PlatformSoftwareUpdateActionAttachmentSchema(Schema):
    class Meta:
        type_ = "platform_software_update_action_attachment"
        self_view = "api.platform_software_update_action_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.platform_software_update_action_attachment_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        self_view="api.platform_software_update_action_attachment_action",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_software_update_action_attachment_detail",
        related_view_kwargs={"id": "<id>"},
        schema="PlatformSoftwareUpdateActionSchema",
        type_="platform_software_update_action",
        id_field="id",
    )
    attachment = Relationship(
        self_view="api.platform_software_update_action_attachment_attachment",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_attachment_detail",
        related_view_kwargs={"id": "<id>"},
        schema="PlatformAttachmentSchema",
        type_="platform_attachment",
        id_field="id",
    )
