from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class PlatformAttachmentSchema(Schema):
    """Explicit schema for platform attachments."""

    class Meta:
        """Meta class for the PlatformAttachmentSchema."""

        type_ = "platform_attachment"
        self_view = "api.platform_attachment_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    label = fields.Str(allow_none=True)
    url = fields.Str(required=True)

    platform = Relationship(
        self_view="api.platform_attachment_platform",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<platform_id>"},
        include_resource_linkage=True,
        type_="platform",
        schema="PlatformSchema",
        id_field="id",
    )
