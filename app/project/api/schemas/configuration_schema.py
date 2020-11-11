from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship

from project.api.serializer.configuration_hierarchy_field import (
    ConfigurationHierarchyField,
)


class ConfigurationSchema(Schema):
    """
    This class create a schema for a configuration

    """

    class Meta:
        type_ = "configuration"
        self_view = "configuration_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True, dump_only=True)
    start_date = fields.DateTime(allow_none=True)
    end_date = fields.DateTime(allow_none=True)
    location_type = fields.String(required=True)
    longitude = fields.Float(allow_none=True)
    latitude = fields.Float(allow_none=True)
    elevation = fields.Float(allow_none=True)
    project_uri = fields.String(allow_none=True)
    project_name = fields.String(allow_none=True)
    label = fields.String(allow_none=True)
    status = fields.String(default="draft", allow_none=True)
    hierarchy = ConfigurationHierarchyField(allow_none=True)

    longitude_src_device_property = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="device_property_detail",
        related_view_kwargs={"id": "<longitude_src_device_property_id>"},
        type_="device_property",
        schema="DevicePropertySchema",
    )

    latitude_src_device_property = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="device_property_detail",
        related_view_kwargs={"id": "<latitude_src_device_property_id>"},
        type_="device_property",
        schema="DevicePropertySchema",
    )

    elevation_src_device_property = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="device_property_detail",
        related_view_kwargs={"id": "<elevation_src_device_property_id>"},
        type_="device_property",
        schema="DevicePropertySchema",
    )

    contacts = Relationship(
        attribute="contacts",
        self_view="configuration_contacts",
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
        self_view="configuration_platforms",
        self_view_kwargs={"id": "<id>"},
        related_view="configuration_platform_list",
        related_view_kwargs={"configuration_id": "<id>"},
        many=True,
        schema="ConfigurationPlatformSchema",
        type_="configuration_platform",
        id_field="id",
    )

    configuration_devices = Relationship(
        attribute="configuration_devices",
        self_view="configuration_devices",
        self_view_kwargs={"id": "<id>"},
        realted_view="configuration_device_list",
        related_view_kwargs={"configuration_id": "<id>"},
        many=True,
        schema="ConfigurationDeviceSchema",
        type="configuration_device",
        id_field="id",
    )
