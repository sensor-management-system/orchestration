# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Module for the site image schema."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class SiteImageSchema(Schema):
    """Schema for the site images."""

    class Meta:
        """Metaclass for the SiteImageSchema."""

        type_ = "site_image"
        self_view = "api.site_image_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.site_image_list"

    id = fields.Integer(as_string=True)
    order_index = fields.Integer(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    site_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    site = Relationship(
        related_view="api.site_detail",
        related_view_kwargs={"id": "<site_id>"},
        include_resource_linkage=True,
        type_="site",
        schema="SiteSchema",
        id_field="id",
    )

    attachment_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    attachment = Relationship(
        related_view="api.site_attachment_detail",
        related_view_kwargs={"id": "<attachment_id>"},
        include_resource_linkage=True,
        type_="site_attachment",
        schema="SiteAttachmentSchema",
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
