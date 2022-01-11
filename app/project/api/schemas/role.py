from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema


class RoleSchema(Schema):
    """
    This class create a schema for an event.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = "role"
        self_view = "api.roles_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.roles_list"

    id = fields.Integer(as_string=True)
    name = fields.Str(required=True)
    uri = fields.Str(required=True)
