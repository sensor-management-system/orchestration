# SPDX-FileCopyrightText: 2020 - 2024
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Schema class for the device properties."""

from marshmallow import Schema as MarshmallowSchema
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class InnerDevicePropertySchema(MarshmallowSchema):
    """
    Schema for device properties meant to be included in another schema.

    This is the very same class as DevicePropertySchema,
    but it uses just a normal marshmallow schema in order
    to support its usage as a nested element within the
    devices schema.
    """

    class Meta:
        """Meta class of the InnerDevicePropertySchema."""

        type_ = "property"

    id = fields.Integer(as_string=True)
    measuring_range_min = fields.Float(allow_none=True)
    measuring_range_max = fields.Float(allow_none=True)
    failure_value = fields.Float(allow_none=True)
    accuracy = fields.Float(allow_none=True)
    label = fields.Str(allow_none=True)
    unit_uri = fields.Str(allow_none=True)
    unit_name = fields.Str(allow_none=True)
    compartment_uri = fields.Str(allow_none=True)
    compartment_name = fields.Str(allow_none=True)
    property_uri = fields.Str(allow_none=True)
    property_name = fields.Str(required=True)
    sampling_media_uri = fields.Str(allow_none=True)
    sampling_media_name = fields.Str(allow_none=True)
    resolution = fields.Float(allow_none=True)
    resolution_unit_uri = fields.String(allow_none=True)
    resolution_unit_name = fields.String(allow_none=True)

    @staticmethod
    def dict_serializer(obj):
        """Convert the object to a dict."""
        if obj is not None:
            return {
                "label": obj.label,
                "unit_name": obj.unit_name,
                "unit_uri": obj.unit_uri,
                "compartment_name": obj.compartment_name,
                "compartment_uri": obj.compartment_uri,
                "property_name": obj.property_name,
                "property_uri": obj.property_uri,
                "sample_medium_name": obj.sampling_media_name,
                "sample_medium_uri": obj.sampling_media_uri,
                "measuring_range_min": obj.measuring_range_min,
                "measuring_range_max": obj.measuring_range_max,
                "failure_value": obj.failure_value,
                "resolution": obj.resolution,
                "resolution_unit_uri": obj.resolution_unit_uri,
                "resolution_unit_name": obj.resolution_unit_name,
            }


class DevicePropertySchema(Schema):
    """
    This class create a schema for a property.

    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        """Meta class for the DevicePropertySchema."""

        type_ = "device_property"
        self_view = "api.device_property_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    measuring_range_min = fields.Float(allow_none=True)
    measuring_range_max = fields.Float(allow_none=True)
    failure_value = fields.Float(allow_none=True)
    accuracy = fields.Float(allow_none=True)
    label = fields.Str(allow_none=True)
    accuracy_unit_uri = fields.String(allow_none=True)
    accuracy_unit_name = fields.String(allow_none=True)
    unit_uri = fields.Str(allow_none=True)
    unit_name = fields.Str(allow_none=True)
    compartment_uri = fields.Str(allow_none=True)
    compartment_name = fields.Str(allow_none=True)
    property_uri = fields.Str(allow_none=True)
    property_name = fields.Str(allow_none=True)
    sampling_media_uri = fields.Str(allow_none=True)
    sampling_media_name = fields.Str(allow_none=True)
    resolution = fields.Float(allow_none=True)
    resolution_unit_uri = fields.String(allow_none=True)
    resolution_unit_name = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    aggregation_type_uri = fields.String(allow_none=True)
    aggregation_type_name = fields.String(allow_none=True)
    description = fields.Str(allow_none=True)

    # Adding this field will allow us to filter over the device_id field.
    # Unfortunally it is not possible to use the relationship directly.
    # However, we don't want to allow the user to use it to overwrite,
    # nor we want to put it out as a result.
    device_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
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
