# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Schema classes for the datastream links."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class DatastreamLinkSchema(Schema):
    """
    Schema class for the datastream link.

    Helps to serialize & deserialize for (dicts <-> models) and to validate.
    """

    class Meta:
        """Meta class for the DatastreamLinkSchema."""

        type_ = "datastream_link"
        self_view = "api.datastream_link_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    begin_date = fields.DateTime(allow_none=True)
    end_date = fields.DateTime(allow_none=True)
    datasource_id = fields.Str(required=True)
    datasource_name = fields.Str(allow_none=True)
    thing_id = fields.Str(required=True)
    thing_name = fields.Str(allow_none=True)
    datastream_id = fields.Str(required=True)
    datastream_name = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    license_uri = fields.Str(allow_none=True)
    license_name = fields.Str(allow_none=True)
    aggregation_period = fields.Float(allow_none=True)

    created_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        id_field="id",
        dump_only=True,
    )
    updated_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        id_field="id",
        dump_only=True,
    )
    device_mount_action = Relationship(
        related_view="api.device_mount_action_detail",
        related_view_kwargs={"id": "<device_mount_action_id>"},
        include_resource_linkage=True,
        schema="DeviceMountActionSchema",
        type_="device_mount_action",
        id_field="id",
        required=True,
    )
    device_property = Relationship(
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<device_property_id>"},
        include_resource_linkage=True,
        schema="DevicePropertySchema",
        type_="device_property",
        id_field="id",
        required=True,
    )
    tsm_endpoint = Relationship(
        related_view="api.tsm_endpoint_detail",
        related_view_kwargs={"id": "<tsm_endpoint_id>"},
        include_resource_linkage=True,
        schema="TsmEndpointSchema",
        type_="tsm_endpoint",
        id_field="id",
        required=True,
    )
