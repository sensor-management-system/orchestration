"""Contact schema."""
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class ContactSchema(Schema):
    """
    Schema class for contacts.

    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        """Meta class for contact schema."""

        type_ = "contact"
        self_view = "api.contact_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    given_name = fields.Str(required=True)
    family_name = fields.Str(required=True)
    website = fields.Str(allow_none=True)
    email = fields.Email(required=True)
    active = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    # This relationship should be optional as we want to
    # allow adding extern contacts without user accounts.
    user = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=False,
        schema="UserPublicSchema",
        type_="user",
        id_field="id",
        dump_only=True,
    )
    created_by = Relationship(
        attribute="created_by",
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        dump_only=True,
    )
    updated_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        dump_only=True,
    )

    @staticmethod
    def dict_serializer(obj):
        """Convert the object to a dict."""
        if obj is not None:
            return {
                "given_name": obj.given_name,
                "family_name": obj.family_name,
                "website": obj.website,
                "email": obj.email,
            }
