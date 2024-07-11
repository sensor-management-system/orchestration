# SPDX-FileCopyrightText: 2022 - 2024
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Schemas for the configuration custom fields."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class ConfigurationCustomFieldSchema(Schema):
    """Schema for configuration custom fields."""

    class Meta:
        """Meta class for the ConfigurationCustomFieldSchema."""

        type_ = "configuration_customfield"
        self_view = "api.configuration_customfield_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    key = fields.Str(required=True)
    value = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)

    configuration_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    configuration = Relationship(
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        type_="configuration",
        schema="ConfigurationSchema",
        id_field="id",
    )
