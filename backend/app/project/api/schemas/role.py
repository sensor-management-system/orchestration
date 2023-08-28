# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Schema classes for contact role schemas."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class RoleSchema:
    """Mixin class for common role schema fields."""

    id = fields.Integer(as_string=True)
    role_name = fields.Str(required=True)
    role_uri = fields.Str(required=True)


class DeviceRoleSchema(Schema, RoleSchema):
    """JSON-API compliant data for DeviceRole."""

    class Meta:
        """Meta class for the device role schema."""

        type_ = "device_contact_role"
        self_view = "api.device_contact_role_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.device_contact_role_list"

    device = Relationship(
        self_view="api.device_list",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        include_resource_linkage=True,
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )
    contact = Relationship(
        self_view="api.contact_list",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )


class PlatformRoleSchema(Schema, RoleSchema):
    """JSON-API compliant data for PlatformRole."""

    class Meta:
        """Meta class for the platform role schema."""

        type_ = "platform_contact_role"
        self_view = "api.platform_contact_role_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.platform_contact_role_list"

    platform = Relationship(
        self_view="api.platform_list",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<platform.id>"},
        include_resource_linkage=True,
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    contact = Relationship(
        self_view="api.contact_list",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )


class ConfigurationRoleSchema(Schema, RoleSchema):
    """JSON-API compliant data for ConfigurationRole."""

    class Meta:
        """Meta class for the configuration role schema."""

        type_ = "configuration_contact_role"
        self_view = "api.configuration_contact_role_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.configuration_contact_role_list"

    configuration = Relationship(
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        schema="ConfigurationSchema",
        type_="configuration",
        id_field="id",
    )
    contact = Relationship(
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )


class SiteRoleSchema(Schema, RoleSchema):
    """JSON-API compliant data for SiteRole."""

    class Meta:
        """Meta class for the site role schema."""

        type_ = "site_contact_role"
        self_view = "api.site_contact_role_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.site_contact_role_list"

    site = Relationship(
        related_view="api.site_detail",
        related_view_kwargs={"id": "<site_id>"},
        include_resource_linkage=True,
        schema="SiteSchema",
        type_="site",
        id_field="id",
    )
    contact = Relationship(
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
