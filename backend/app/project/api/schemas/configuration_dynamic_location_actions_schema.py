# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2


"""Schema class for the dynamic location actions."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class ConfigurationDynamicLocationBeginActionSchema(Schema):
    """
    This class creates a schema for a dynamic location action.

    It uses the  marshmallow-jsonapi library that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        """Meta classf for the ConfigurationDynamicLocationBeginActionSchema."""

        type_ = "configuration_dynamic_location_action"
        self_view = "api.configuration_dynamic_location_begin_action_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    begin_date = fields.DateTime(required=True)
    end_date = fields.DateTime(allow_none=True)
    begin_description = fields.Str(allow_none=True)
    end_description = fields.Str(allow_none=True)
    label = fields.Str(allow_none=True)
    epsg_code = fields.Str(allow_none=True)
    elevation_datum_name = fields.Str(allow_none=True)
    elevation_datum_uri = fields.Str(allow_none=True)

    begin_contact = Relationship(
        attribute="begin_contact",
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<begin_contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    end_contact = Relationship(
        attribute="end_contact",
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<end_contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
        allow_none=True,
    )
    configuration_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    configuration = Relationship(
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        type_="configuration",
        schema="ConfigurationSchema",
    )
    x_property_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    x_property = Relationship(
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<x_property_id>"},
        include_resource_linkage=True,
        type_="device_property",
        schema="DevicePropertySchema",
    )
    y_property_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    y_property = Relationship(
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<y_property_id>"},
        include_resource_linkage=True,
        type_="device_property",
        schema="DevicePropertySchema",
    )
    z_property_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    z_property = Relationship(
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<z_property_id>"},
        include_resource_linkage=True,
        type_="device_property",
        schema="DevicePropertySchema",
        allow_none=True,
    )
