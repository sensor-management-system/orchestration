from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class ConfigurationDynamicLocationBeginActionSchema(Schema):
    """
    This class create a schema for a configuration_dynamic_location_begin_action.
    It uses the  marshmallow-jsonapi library that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        type_ = "configuration_dynamic_location_begin_action"
        self_view = "api.configuration_dynamic_location_begin_action_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    begin_date = fields.DateTime(required=True)
    description = fields.Str(allow_none=True)
    epsg_code = fields.Str(allow_none=True)
    elevation_datum_name = fields.Str(allow_none=True)
    elevation_datum_uri = fields.Str(allow_none=True)

    contact = Relationship(
        attribute="contact",
        self_view="api.configuration_dynamic_location_begin_action_contact",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )

    configuration = Relationship(
        self_view="api.configuration_dynamic_location_begin_action_configuration",
        self_view_kwargs={"id": "<id>"},
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        type_="configuration",
        schema="ConfigurationSchema",
    )
    x_property = Relationship(
        self_view="api.configuration_dynamic_location_begin_action_x_property",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<x_property_id>"},
        include_resource_linkage=True,
        type_="device_property",
        schema="DevicePropertySchema",
    )
    y_property = Relationship(
        self_view="api.configuration_dynamic_location_begin_action_y_property",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<y_property_id>"},
        include_resource_linkage=True,
        type_="device_property",
        schema="DevicePropertySchema",
    )
    z_property = Relationship(
        self_view="api.configuration_dynamic_location_begin_action_z_property",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<z_property_id>"},
        include_resource_linkage=True,
        type_="device_property",
        schema="DevicePropertySchema",
    )


class ConfigurationDynamicLocationEndActionSchema(Schema):
    """
    This class create a schema for a configuration_dynamic_location_end_action.
    """

    class Meta:
        type_ = "configuration_dynamic_location_end_action"
        self_view = "api.configuration_dynamic_location_end_action_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    end_date = fields.DateTime(required=True)
    description = fields.Str(allow_none=True)

    contact = Relationship(
        attribute="contact",
        self_view="api.configuration_dynamic_location_end_action_contact",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )

    configuration = Relationship(
        self_view="api.configuration_dynamic_location_end_action_configuration",
        self_view_kwargs={"id": "<id>"},
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        type_="configuration",
        schema="ConfigurationSchema",
    )
