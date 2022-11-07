"""Schema class for device attachments."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class DeviceAttachmentSchema(Schema):
    """
    Explicit schema for device attachments.

    It is indended to use this schema for
    explicit device attachment resources.
    """

    class Meta:
        """Meta class for the DeviceAttachmentSchema."""

        type_ = "device_attachment"
        self_view = "api.device_attachment_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    label = fields.Str(required=True)
    url = fields.Str(required=True)
    is_upload = fields.Bool(dump_only=True)

    device = Relationship(
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        include_resource_linkage=True,
        type_="device",
        schema="DeviceSchema",
        id_field="id",
    )
