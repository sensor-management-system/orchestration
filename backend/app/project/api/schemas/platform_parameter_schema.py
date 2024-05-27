# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Schema class for the platform parameters."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class PlatformParameterSchema(Schema):
    """Schema class for the platform parameters."""

    class Meta:
        """Meta class for the PlatformParameterSchema class."""

        type_ = "platform_parameter"
        self_view = "api.platform_parameter_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    label = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    unit_uri = fields.Str(allow_none=True)
    unit_name = fields.Str(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    platform_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    platform = Relationship(
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<platform_id>"},
        include_resource_linkage=True,
        type_="platform",
        schema="PlatformSchema",
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

    platform_parameter_value_change_actions = Relationship(
        related_view="api.platform_parameter_value_change_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="PlatformParameterValueChangeActionSchema",
        type_="platform_parameter_value_change_action",
        id_field="id",
    )
