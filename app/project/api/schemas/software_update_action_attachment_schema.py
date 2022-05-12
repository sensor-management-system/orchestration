# Define Schema for
# DeviceSoftwareUpdateActionAttachment & PlatformSoftwareUpdateActionAttachment
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class DeviceSoftwareUpdateActionAttachmentSchema(Schema):
    """
    This class create a schema for a DeviceSoftwareUpdateActionAttachment.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        type_ = "device_software_update_action_attachment"
        self_view = "api.device_software_update_action_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.device_software_update_action_attachment_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        related_view="api.device_software_update_action_attachment_detail",
        related_view_kwargs={"id": "<action_id>"},
        include_resource_linkage=True,
        schema="DeviceSoftwareUpdateActionSchema",
        type_="device_software_update_action",
        id_field="id",
    )
    attachment = Relationship(
        related_view="api.device_attachment_detail",
        related_view_kwargs={"id": "<attachment_id>"},
        include_resource_linkage=True,
        schema="DeviceAttachmentSchema",
        type_="device_attachment",
        id_field="id",
    )


class PlatformSoftwareUpdateActionAttachmentSchema(Schema):
    """
    This class create a schema for a platform_software_update_action_attachment.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        type_ = "platform_software_update_action_attachment"
        self_view = "api.platform_software_update_action_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.platform_software_update_action_attachment_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        related_view="api.platform_software_update_action_attachment_detail",
        related_view_kwargs={"id": "<action_id>"},
        include_resource_linkage=True,
        schema="PlatformSoftwareUpdateActionSchema",
        type_="platform_software_update_action",
        id_field="id",
    )
    attachment = Relationship(
        related_view="api.platform_attachment_detail",
        related_view_kwargs={"id": "<attachment_id>"},
        include_resource_linkage=True,
        schema="PlatformAttachmentSchema",
        type_="platform_attachment",
        id_field="id",
    )
