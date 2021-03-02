from marshmallow import Schema as MarshmallowSchema
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class InnerCustomFieldSchema(MarshmallowSchema):
    """
    This class create a schema for a custom field.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = "customfield"

    id = fields.Integer(as_string=True)
    key = fields.Str(required=True)
    value = fields.Str(allow_none=True)

    @staticmethod
    def dict_serializer(obj):
        """Convert the object to a dict."""
        if obj is not None:
            return {
                "key": obj.key,
                "value": obj.value,
            }


class CustomFieldSchema(Schema):
    """Schema for custom fields."""

    class Meta:
        """Meta class for the CustomFieldSchema."""

        type_ = "customfield"
        self_view = "api.customfield_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    key = fields.Str(required=True)
    value = fields.Str(allow_none=True)

    device = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        type_="device",
    )
