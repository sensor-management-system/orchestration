from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class ConfigurationAttachmentSchema(Schema):
    """
    Explicit schema for configuration attachments.
    """

    class Meta:
        """Meta class for the ConfigurationAttachmentSchema."""

        type_ = "configuration_attachment"
        self_view = "api.configuration_attachment_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    label = fields.Str(required=True)
    url = fields.Str(required=True)

    configuration = Relationship(
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        type_="configuration",
        schema="ConfigurationSchema",
        id_field="id",
    )
