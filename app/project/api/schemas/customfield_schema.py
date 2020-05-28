from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema
from project.api.schemas.base_schema import \
    set_device_relationship_schema


class CustomFieldSchema(Schema):
    """
    This class create a schema for a custom field.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = 'customfield'
        self_view = 'customfields_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    key = fields.Str(required=True)
    value = fields.Str(required=True)

    device = set_device_relationship_schema('customfields')
