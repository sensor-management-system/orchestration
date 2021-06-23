from marshmallow import Schema as MarshmallowSchema
from marshmallow_jsonapi import fields


class AttachmentSchema(MarshmallowSchema):
    """
    This class create a schema for a attachment.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = "attachment"

    id = fields.Integer(as_string=True)
    label = fields.Str(allow_none=True)
    url = fields.Str(required=True)

    @staticmethod
    def dict_serializer(obj):
        """Convert the object to an dict."""
        if obj is not None:
            return {"label": obj.label, "url": obj.url}
