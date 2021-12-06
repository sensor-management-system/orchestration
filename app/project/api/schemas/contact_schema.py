from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class ContactSchema(Schema):
    """
    This class create a schema for a contact.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = "contact"
        self_view = "api.contact_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    given_name = fields.Str(required=True)
    family_name = fields.Str(required=True)
    website = fields.Str(allow_none=True)
    email = fields.Email(required=True)
    active = fields.Boolean(dump_only=True)

    platforms = Relationship(
        attribute="platforms",
        related_view="api.contact_platforms",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=False,
        many=True,
        schema="PlatformPublicSchema",
        type_="platform",
        id_field="id",
    )
    configurations = Relationship(
        attribute="configurations",
        related_view="api.contact_configurations",
        related_view_kwargs={"id": "<id>"},
        many=True,
        include_resource_linkage=False,
        schema="ConfigurationPublicSchema",
        type_="configuration",
        id_field="id",
    )
    devices = Relationship(
        attribute="devices",
        related_view="api.contact_devices",
        related_view_kwargs={"id": "<id>"},
        many=True,
        include_resource_linkage=False,
        schema="DevicePublicSchema",
        type_="device",
        id_field="id",
    )
    # This relationship should be optional as we want to
    # allow adding extern contacts without user accounts.
    user = Relationship(
        self_view="api.contact_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<user.id>"},
        include_resource_linkage=False,
        schema="UserPublicSchema",
        type_="user",
        id_field="id",
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
