# SPDX-FileCopyrightText: 2020 - 2022
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Schema class for configurations."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from ..schemas.contact_schema import ContactSchema


class ConfigurationSchema(Schema):
    """This class create a schema for a configuration."""

    class Meta:
        """Meta class for the configuration schema."""

        type_ = "configuration"
        self_view = "api.configuration_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    start_date = fields.DateTime(allow_none=True)
    end_date = fields.DateTime(allow_none=True)
    label = fields.String(allow_none=True)
    project = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    status = fields.String(default="draft", allow_none=True)
    cfg_permission_group = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_internal = fields.Boolean(allow_none=True)
    is_public = fields.Boolean(allow_none=True)
    archived = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    update_description = fields.Str(dump_only=True)
    persistent_identifier = fields.Str(allow_none=True)
    contacts = Relationship(
        attribute="contacts",
        related_view="api.contact_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    generic_configuration_actions = Relationship(
        related_view="api.generic_configuration_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="GenericConfigurationActionSchema",
        type_="generic_configuration_action",
        id_field="id",
    )
    device_mount_actions = Relationship(
        related_view="api.device_mount_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="DeviceMountActionSchema",
        type_="device_mount_action",
        id_field="id",
    )
    platform_mount_actions = Relationship(
        related_view="api.platform_mount_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="PlatformMountActionSchema",
        type_="platform_mount_actions",
        id_field="id",
    )
    configuration_static_location_actions = Relationship(
        attribute="configuration_static_location_begin_actions",
        related_view="api.configuration_static_location_begin_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="ConfigurationStaticLocationBeginActionSchema",
        type_="configuration_static_location_action",
        id_field="id",
    )
    configuration_dynamic_location_actions = Relationship(
        attribute="configuration_dynamic_location_begin_actions",
        related_view="api.configuration_dynamic_location_begin_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="ConfigurationDynamicLocationBeginActionSchema",
        type_="configuration_dynamic_location_action",
        id_field="id",
    )
    created_by = Relationship(
        self_view="api.user_list",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        dump_only=True,
    )
    updated_by = Relationship(
        self_view="api.user_list",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        dump_only=True,
    )
    configuration_customfields = Relationship(
        related_view="api.configuration_customfield_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="ConfigurationCustomFieldSchema",
        type_="configuration_customfield",
        id_field="id",
    )
    configuration_parameters = Relationship(
        related_view="api.configuration_parameter_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="ConfigurationParameterSchema",
        type_="configuration_parameter",
        id_field="id",
    )
    site = Relationship(
        related_view="api.site_detail",
        related_view_kwargs={"id": "<site_id>"},
        include_resource_linkage=True,
        type_="site",
        schema="SiteSchema",
        id_field="id",
        allow_none=True,
    )

    @staticmethod
    def nested_dict_serializer(configuration):
        """Serialize the object to a nested dict."""
        return ConfigurationToNestedDictSerializer().to_nested_dict(configuration)


class ConfigurationToNestedDictSerializer:
    """Some other serializer, so that we include it somewhere."""

    @staticmethod
    def to_nested_dict(configuration):
        """
        Convert the configuration-object to a nested dict.

        :param configuration:
        :return:
        """
        if configuration is not None:
            return {
                "label": configuration.label,
                "status": configuration.status,
                "contacts": [
                    ContactSchema().dict_serializer(c) for c in configuration.contacts
                ],
                "start_date": configuration.start_date,
                "end_date": configuration.end_date,
            }


class ConfigurationSchemaForOnlyId(Schema):
    """Schema that just returns the id of the configuration."""

    class Meta:
        """Meta class for ConfigurationSchemaForOnlyId."""

        type_ = "configuration"
        self_view = "api.configuration_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.configuration_list"

    id = fields.Integer(as_string=True)
