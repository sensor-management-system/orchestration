# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Module for the manufacturer model schema."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from .export_control_schema import PublicExportControlSchema


class ManufacturerModelSchema(Schema):
    """Schema for the manufacturer models."""

    class Meta:
        """Metaclass for the ManufacturerModelSchema."""

        type_ = "manufacturer_model"
        self_view = "api.manufacturer_model_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.manufacturer_model_list"

    id = fields.Integer(as_string=True)
    manufacturer_name = fields.Str(required=True)
    model = fields.Str(required=True)
    external_system_name = fields.Str(allow_none=True)
    external_system_url = fields.Str(allow_none=True)
    export_control = Relationship(
        related_view="api.export_control_list",
        related_view_kwargs={"manufacturer_model_id": "<id>"},
        include_resource_linkage=True,
        type_="export_control",
        schema=PublicExportControlSchema,
        id_field="id",
    )
