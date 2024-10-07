# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Module for the involved device for datastream link schema."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class InvolvedDeviceForDatastreamLinkSchema(Schema):
    """Schema for the involved devices in datastream links."""

    class Meta:
        """Metaclass for the InvolvedDeviceForDatastreamLinkSchema."""

        type_ = "involved_device_for_datastream_link"
        self_view = "api.involved_device_for_datastream_link_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.involved_device_for_datastream_link_list"

    id = fields.Integer(as_string=True)
    order_index = fields.Integer(allow_none=True)

    device_id = fields.Integer(dump_only=True, load_only=True, as_string=True)

    device = Relationship(
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        include_resource_linkage=True,
        type_="device",
        schema="DeviceSchema",
        id_field="id",
    )

    datastream_link_id = fields.Integer(dump_only=True, load_only=True, as_string=True)

    datastream_link = Relationship(
        related_view="api.datastream_link_detail",
        related_view_kwargs={"id": "<datastream_link_id>"},
        include_resource_linkage=True,
        type_="datastream_link",
        schema="DatastreamLinkSchema",
        id_field="id",
    )
