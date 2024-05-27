# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Schema class for export control attachments."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class ExportControlAttachmentSchema(Schema):
    """JSON API schema for export control attachments."""

    class Meta:
        """Meta class for the ExportControlAttachmentSchema."""

        type_ = "export_control_attachment"
        self_view = "api.export_control_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.export_control_attachment_list"

    id = fields.Integer(as_string=True)
    label = fields.Str(required=True)
    url = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    is_upload = fields.Bool(dump_only=True)
    is_export_control_only = fields.Boolean(required=True)
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
