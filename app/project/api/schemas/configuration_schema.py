from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship
from project.api.schemas.contact_schema import ContactSchema
from project.api.schemas.device_property_schema import DevicePropertySchema


class ConfigurationSchema(Schema):
    """
    This class create a schema for a configuration

    """

    class Meta:
        type_ = "configuration"
        self_view = "configuration_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True, dump_only=True)
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    location_type = fields.String(required=True)
    longitude = fields.Float()
    latitude = fields.Float()
    elevation = fields.Float()
    project_uri = fields.String()
    project_name = fields.String()

    longitude_src_device_property = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="device_property_detail",
        related_view_kwargs={"id": "<longitude_src_device_property_id>"},
        type_="device_property",
    )

    latitude_src_device_property = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="device_property_detail",
        related_view_kwargs={"id": "<latitude_src_device_property_id>"},
        type_="device_property",
    )

    elevation_src_device_property = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="device_property_detail",
        related_view_kwargs={"id": "<elevation_src_device_property_id>"},
        type_="device_property",
    )

    contacts = Relationship(
        attribute="contacts",
        self_view_kwargs={"id": "<id>"},
        related_view="contact_list",
        related_view_kwargs={"configuration_id": "<id>"},
        many=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )

    configuration_platforms = Relationship(
        attribute="configuration_platforms",
        self_view_kwargs={"id": "<id>"},
        related_view="configuration_platform_list",
        related_view_kwargs={"configuration_id": "<id>"},
        many=True,
        schema="ConfigurationPlatformSchema",
        type_="configuration_platform",
        id_field="id",
    )

    # configuration_devices = fields.Nested(
    #     "ConfigurationDeviceSchema", many=True, allow_none=True
    # )

    configuration_devices = Relationship(
        attribute="configuration_devices",
        self_view_kwargs={"id": "<id>"},
        related_view="configuration_device_list",
        related_view_kwargs={"configuration_id": "<id>"},
        many=True,
        schema="ConfigurationDeviceSchema",
        type_="configuration_device",
        id_field="id",
    )
