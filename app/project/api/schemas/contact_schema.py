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
        include_resource_linkage=True,
        many=True,
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    configurations = Relationship(
        attribute="configurations",
        related_view="api.contact_configurations",
        related_view_kwargs={"id": "<id>"},
        many=True,
        include_resource_linkage=True,
        schema="ConfigurationSchema",
        type_="configuration",
        id_field="id",
    )
    devices = Relationship(
        attribute="devices",
        related_view="api.contact_devices",
        related_view_kwargs={"id": "<id>"},
        many=True,
        include_resource_linkage=True,
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )
    # This relationship should be optional as we want to
    # allow to add extern contacts without user accounts.
    user = Relationship(
        required=False,
        allow_none=True,
        self_view="api.contact_user",
        self_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        schema="UserSchema",
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
