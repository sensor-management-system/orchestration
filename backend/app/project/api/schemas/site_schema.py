# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Schema for the sites."""
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from ..serializer.fields.wkt_polygon_field import WktPolygonField


class SiteSchema(Schema):
    """Site schema class."""

    class Meta:
        """Meta class for the site schema."""

        type_ = "site"
        self_view = "api.site_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.site_list"

    id = fields.Integer(as_string=True)
    persistent_identifier = fields.Str(allow_none=True)
    label = fields.Str(allow_none=True)
    geometry = WktPolygonField(allow_none=True)
    description = fields.Str(allow_none=True)
    epsg_code = fields.Str(allow_none=True)
    is_internal = fields.Boolean(allow_none=True)
    is_public = fields.Boolean(allow_none=True)
    group_ids = fields.Field(many=True, allow_none=True)
    archived = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    update_description = fields.Str(dump_only=True)
    street = fields.Str(allow_none=True)
    street_number = fields.Str(allow_none=True)
    city = fields.Str(allow_none=True)
    zip_code = fields.Str(allow_none=True)
    country = fields.Str(allow_none=True)
    building = fields.Str(allow_none=True)
    room = fields.Str(allow_none=True)
    site_type_uri = fields.Str(allow_none=True)
    site_type_name = fields.Str(allow_none=True)
    site_usage_uri = fields.Str(allow_none=True)
    site_usage_name = fields.Str(allow_none=True)
    elevation = fields.Float(allow_none=True)
    elevation_datum_name = fields.Str(allow_none=True)
    elevation_datum_uri = fields.Str(allow_none=True)
    website = fields.Str(allow_none=True)
    keywords = fields.Field(many=True, allow_none=True)

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
        attribute="updated_by",
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        dump_only=True,
    )
    # We don't include the sites configurations in the schema.
    # Background is that those can have different visibility states.
    # When the site is public, but one of the configurations is internal,
    # then the 'include' mechanism would also show the data of internal
    # configuration - even if the request was made without a login.

    outer_site = Relationship(
        related_view="api.site_detail",
        related_view_kwargs={"id": "<outer_site_id>"},
        include_resource_linkage=True,
        type_="site",
        schema="SiteSchema",
        id_field="id",
        allow_none=True,
    )
    site_images = Relationship(
        related_view="api.site_image_list",
        related_view_kwargs={"filter[site_id]": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="SiteImageSchema",
        type_="site_image",
        id_field="id",
    )
    site_attachments = Relationship(
        related_view="api.site_attachment_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="SiteAttachmentSchema",
        type_="site_attachment",
        id_field="id",
    )
