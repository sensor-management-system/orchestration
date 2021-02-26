from marshmallow import Schema as MarshmallowSchema
from marshmallow_jsonapi import fields


class CustomFieldSchema(MarshmallowSchema):
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
