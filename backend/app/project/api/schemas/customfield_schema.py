# SPDX-FileCopyrightText: 2020 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Schema for the customfields (for devices)."""

from marshmallow import Schema as MarshmallowSchema
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class InnerCustomFieldSchema(MarshmallowSchema):
    """
    This class create a schema for a custom field.

    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        """Meta class for an inner schema to be nested in some other one."""

        type_ = "customfield"

    id = fields.Integer(as_string=True)
    key = fields.Str(required=True)
    value = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)

    @staticmethod
    def dict_serializer(obj):
        """Convert the object to a dict."""
        if obj is not None:
            return {
                "key": obj.key,
                "value": obj.value,
            }


class CustomFieldSchema(Schema):
    """Schema for custom fields."""

    class Meta:
        """Meta class for the CustomFieldSchema."""

        type_ = "customfield"
        self_view = "api.customfield_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    key = fields.Str(required=True)
    value = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)

    device_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    device = Relationship(
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        include_resource_linkage=True,
        type_="device",
        schema="DeviceSchema",
        id_field="id",
    )
