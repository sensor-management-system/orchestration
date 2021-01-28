from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class EventSchema(Schema):
    """
    This class create a schema for an event.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = "event"
        self_view = "api.event_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.event_list"

    id = fields.Integer(as_string=True)
    description = fields.Str(required=True)
    timestamp = fields.DateTime(required=True)
    user = Relationship(
        self_view="api.event_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.event_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        id_field="id",
    )
