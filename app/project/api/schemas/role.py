from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class RoleSchema:
    id = fields.Integer(as_string=True)
    role_name = fields.Str(required=True)
    role_uri = fields.Str(required=True)


class DeviceRoleSchema(Schema, RoleSchema):
    """
    JSON API-compliant data für DeviceRole
    """

    class Meta:
        type_ = "device_contact_role"
        self_view = "api.device_contact_role_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.device_contact_role_list"

    device = Relationship(
        self_view="api.device_contact_roles",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        include_resource_linkage=True,
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )
    contact = Relationship(
        self_view="api.contact_roles_device",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )


class PlatformRoleSchema(Schema, RoleSchema):
    """
    JSON API-compliant data für PlatformRole
    """

    class Meta:
        type_ = "platform_contact_role"
        self_view = "api.platform_contact_role_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.platform_contact_role_list"

    platform = Relationship(
        self_view="api.platform_contact_roles",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<platform.id>"},
        include_resource_linkage=True,
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    contact = Relationship(
        self_view="api.contact_roles_platform",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )


class ConfigurationRoleSchema(Schema, RoleSchema):
    """
    JSON API-compliant data für ConfigurationRole
    """

    class Meta:
        type_ = "configuration_contact_role"
        self_view = "api.configuration_contact_role_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.configuration_contact_role_list"

    configuration = Relationship(
        self_view="api.configuration_contact_roles",
        self_view_kwargs={"id": "<id>"},
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        schema="ConfigurationSchema",
        type_="configuration",
        id_field="id",
    )
    contact = Relationship(
        self_view="api.contact_roles_configuration",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
