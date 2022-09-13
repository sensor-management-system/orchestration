from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class UserSchema(Schema):
    """
    This class create a schema for a user.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = "user"
        self_view = "api.user_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.user_list"

    id = fields.Integer(as_string=True)
    subject = fields.Str(required=True)

    contact = Relationship(
        attribute="contact",
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )


class UserPublicSchema(Schema):
    class Meta:
        type_ = "user"
        self_view = "api.user_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.user_list"

    id = fields.Integer(as_string=True)
