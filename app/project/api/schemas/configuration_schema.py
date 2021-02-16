from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from project.api.schemas.configuration_device_schema import ConfigurationDeviceSchema
from project.api.schemas.configuration_platform_schema import (
    ConfigurationPlatformSchema,
)
from project.api.schemas.contact_schema import ContactSchema
from project.api.schemas.device_property_schema import InnerDevicePropertySchema
from project.api.serializer.configuration_hierarchy_field import (
    ConfigurationHierarchyField,
)


class ConfigurationSchema(Schema):
    """
    This class create a schema for a configuration

    """

    class Meta:
        type_ = "configuration"
        self_view = "api.configuration_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
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

    src_longitude = Relationship(
        attribute="src_longitude",
        self_view="api.configuration_src_longitude",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<longitude_src_device_property_id>"},
        type_="device_property",
        schema="DevicePropertySchema",
    )

    src_latitude = Relationship(
        attribute="src_latitude",
        self_view="api.configuration_src_latitude",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<latitude_src_device_property_id>"},
        type_="device_property",
        schema="DevicePropertySchema",
    )

    src_elevation = Relationship(
        attribute="src_elevation",
        self_view="api.configuration_src_elevation",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<elevation_src_device_property_id>"},
        type_="device_property",
        schema="DevicePropertySchema",
    )

    contacts = Relationship(
        attribute="contacts",
        self_view="api.configuration_contacts",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_list",
        related_view_kwargs={"configuration_id": "<id>"},
        many=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    configuration_platforms = Relationship(
        attribute="configuration_platforms",
        self_view="api.configuration_platforms",
        self_view_kwargs={"id": "<id>"},
        related_view="api.configuration_platform_list",
        related_view_kwargs={"configuration_id": "<id>"},
        many=True,
        schema="ConfigurationPlatformSchema",
        type_="configuration_platform",
        id_field="id",
    )

    configuration_devices = Relationship(
        attribute="configuration_devices",
        self_view="api.configuration_devices",
        self_view_kwargs={"id": "<id>"},
        realted_view="api.configuration_device_list",
        related_view_kwargs={"configuration_id": "<id>"},
        many=True,
        schema="ConfigurationDeviceSchema",
        type="configuration_device",
        id_field="id",
    )

    @staticmethod
    def nested_dict_serializer(configuration):
        """serialize the object to a nested dict."""
        return ConfigurationToNestedDictSerializer().to_nested_dict(configuration)


class ConfigurationToNestedDictSerializer:
    @staticmethod
    def to_nested_dict(configuration):
        """
        Convert the configuration-object to a nested dict.
        :param configuration:
        :return:
        """
        if configuration is not None:
            configuration_platforms = []
            configuration_devices = []
            for cd in configuration.configuration_devices:
                configuration_device = (
                    ConfigurationDeviceSchema().nested_dict_serializer(cd)
                )
                configuration_devices.append(configuration_device)
            for cp in configuration.configuration_platforms:
                configuration_platform = (
                    ConfigurationPlatformSchema().nested_dict_serializer(cp)
                )
                configuration_platforms.append(configuration_platform)
            return {
                "label": configuration.label,
                "status": configuration.status,
                "location_type": configuration.location_type,
                "project_uri": configuration.project_uri,
                "project_name": configuration.project_name,
                "contacts": [
                    ContactSchema().dict_serializer(c) for c in configuration.contacts
                ],
                "start_date": configuration.start_date,
                "end_date": configuration.end_date,
                "configuration_platforms": configuration_platforms,
                "configuration_devices": configuration_devices,
                "longitude": configuration.longitude,
                "src_longitude": InnerDevicePropertySchema().dict_serializer(
                    configuration.src_longitude
                ),
                "latitude": configuration.latitude,
                "src_latitude": InnerDevicePropertySchema().dict_serializer(
                    configuration.src_latitude
                ),
                "elevation": configuration.elevation,
                "src_elevation": InnerDevicePropertySchema().dict_serializer(
                    configuration.src_elevation
                ),
            }
