# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Schema class for the device parameters."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class DeviceParameterSchema(Schema):
    """Schema class for the device parameters."""

    class Meta:
        """Meta class for the DeviceParameterSchema class."""

        type_ = "device_parameter"
        self_view = "api.device_parameter_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    label = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    unit_uri = fields.Str(allow_none=True)
    unit_name = fields.Str(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    device = Relationship(
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        include_resource_linkage=True,
        type_="device",
        schema="DeviceSchema",
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

    device_parameter_value_change_actions = Relationship(
        related_view="api.device_parameter_value_change_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="DeviceParameterValueChangeActionSchema",
        type_="device_parameter_value_change_action",
        id_field="id",
    )
