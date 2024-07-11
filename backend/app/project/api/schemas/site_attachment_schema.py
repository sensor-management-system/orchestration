# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Schema class for site attachments."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class SiteAttachmentSchema(Schema):
    """Explicit schema for site attachments."""

    class Meta:
        """Meta class for the SiteAttachmentSchema."""

        type_ = "site_attachment"
        self_view = "api.site_attachment_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    label = fields.Str(required=True)
    url = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    is_upload = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    site_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    site = Relationship(
        related_view="api.site_detail",
        related_view_kwargs={"id": "<site_id>"},
        include_resource_linkage=True,
        type_="site",
        schema="SiteSchema",
        id_field="id",
    )
    site_images = Relationship(
        related_view="api.site_image_list",
        related_view_kwargs={"filter[attachment_id]": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="SiteImageSchema",
        type_="site_image",
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
