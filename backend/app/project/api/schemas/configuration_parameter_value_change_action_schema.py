# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Schema class for the configuration parameter value change actions."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class ConfigurationParameterValueChangeActionSchema(Schema):
    """Schema class for the configuration parameter value change actions."""

    class Meta:
        """Meta class for the ConfigurationParameterValueChangeActionSchema class."""

        type_ = "configuration_parameter_value_change_action"
        self_view = "api.configuration_parameter_value_change_action_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    value = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    date = fields.DateTime(required=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    contact = Relationship(
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    configuration_parameter = Relationship(
        related_view="api.configuration_parameter_detail",
        related_view_kwargs={"id": "<configuration_parameter_id>"},
        include_resource_linkage=True,
        type_="configuration_parameter",
        schema="ConfigurationParameterSchema",
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
