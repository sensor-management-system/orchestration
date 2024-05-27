# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Schema class for the configuration parameters."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class ConfigurationParameterSchema(Schema):
    """Schema class for the configuration parameters."""

    class Meta:
        """Meta class for the ConfigurationParameterSchema class."""

        type_ = "configuration_parameter"
        self_view = "api.configuration_parameter_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    label = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    unit_uri = fields.Str(allow_none=True)
    unit_name = fields.Str(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    configuration_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    configuration = Relationship(
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        type_="configuration",
        schema="ConfigurationSchema",
        id_field="id",
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

    configuration_parameter_value_change_actions = Relationship(
        related_view="api.configuration_parameter_value_change_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="ConfigurationParameterValueChangeActionSchema",
        type_="configuration_parameter_value_change_action",
        id_field="id",
    )
