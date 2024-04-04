# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Module for the manufacturer model schema."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class ExportControlSchema(Schema):
    """Schema for the export control data."""

    class Meta:
        """Metaclass for the ExportControlSchema."""

        type_ = "export_control"
        self_view = "api.export_control_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.export_control_list"

    id = fields.Integer(as_string=True)
    dual_use = fields.Boolean(allow_none=True)
    export_control_classification_number = fields.Str(allow_none=True)
    customs_tariff_number = fields.Str(allow_none=True)
    additional_information = fields.Str(allow_none=True)
    internal_note = fields.Str(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    manufacturer_model_id = fields.Integer(
        dump_only=True, load_only=True, as_string=True
    )
    manufacturer_model = Relationship(
        related_view="api.manufacturer_model_detail",
        related_view_kwargs={"id": "<manufacturer_model_id>"},
        include_resource_linkage=True,
        type_="manufacturer_model",
        schema="ManufacturerModelSchema",
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


class PublicExportControlSchema(Schema):
    """Schema for the export control data with only public fields."""

    class Meta:
        """Metaclass for the ExportControlSchema."""

        type_ = "export_control"
        self_view = "api.export_control_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.export_control_list"

    id = fields.Integer(as_string=True)
    dual_use = fields.Boolean(allow_none=True)
    export_control_classification_number = fields.Str(allow_none=True)
    customs_tariff_number = fields.Str(allow_none=True)
    additional_information = fields.Str(allow_none=True)
    # no internal note field

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    manufacturer_model_id = fields.Integer(
        dump_only=True, load_only=True, as_string=True
    )
    manufacturer_model = Relationship(
        related_view="api.manufacturer_model_detail",
        related_view_kwargs={"id": "<manufacturer_model_id>"},
        include_resource_linkage=True,
        type_="manufacturer_model",
        schema="ManufacturerModelSchema",
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
