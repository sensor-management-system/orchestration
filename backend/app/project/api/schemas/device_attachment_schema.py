# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Schema class for device attachments."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class DeviceAttachmentSchema(Schema):
    """
    Explicit schema for device attachments.

    It is indended to use this schema for
    explicit device attachment resources.
    """

    class Meta:
        """Meta class for the DeviceAttachmentSchema."""

        type_ = "device_attachment"
        self_view = "api.device_attachment_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    label = fields.Str(required=True)
    url = fields.Str(required=True)
    is_upload = fields.Bool(dump_only=True)
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
