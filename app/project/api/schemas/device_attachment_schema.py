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
    label = fields.Str(allow_none=True)
    url = fields.Str(required=True)

    device = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        type_="device",
        schema="DeviceSchema",
        id_field="id"
    )
