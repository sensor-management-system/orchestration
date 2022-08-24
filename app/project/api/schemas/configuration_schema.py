from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from ..schemas.contact_schema import ContactSchema
from ..schemas.device_property_schema import InnerDevicePropertySchema


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
    location_type = fields.String(allow_none=True)
    longitude = fields.Float(allow_none=True)
    latitude = fields.Float(allow_none=True)
    elevation = fields.Float(allow_none=True)
    project_uri = fields.String(allow_none=True)
    project_name = fields.String(allow_none=True)
    label = fields.String(allow_none=True)
    status = fields.String(default="draft", allow_none=True)
    cfg_permission_group = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_internal = fields.Boolean(allow_none=True)
    is_public = fields.Boolean(allow_none=True)
    update_description = fields.Str(dump_only=True)
    src_longitude = Relationship(
        attribute="src_longitude",
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<longitude_src_device_property_id>"},
        include_resource_linkage=True,
        type_="device_property",
        schema="DevicePropertySchema",
    )

    src_latitude = Relationship(
        attribute="src_latitude",
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<latitude_src_device_property_id>"},
        include_resource_linkage=True,
        type_="device_property",
        schema="DevicePropertySchema",
    )

    src_elevation = Relationship(
        attribute="src_elevation",
        related_view="api.device_property_detail",
        related_view_kwargs={"id": "<elevation_src_device_property_id>"},
        include_resource_linkage=True,
        type_="device_property",
        schema="DevicePropertySchema",
    )

    contacts = Relationship(
        attribute="contacts",
        related_view="api.contact_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    generic_configuration_actions = Relationship(
        related_view="api.generic_configuration_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="GenericConfigurationActionSchema",
        type_="generic_configuration_action",
        id_field="id",
    )
    device_mount_actions = Relationship(
        related_view="api.device_mount_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="DeviceMountActionSchema",
        type_="device_mount_action",
        id_field="id",
    )
    platform_mount_actions = Relationship(
        related_view="api.platform_mount_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="PlatformMountActionSchema",
        type_="platform_mount_actions",
        id_field="id",
    )
    configuration_static_location_actions = Relationship(
        attribute="configuration_static_location_begin_actions",
        related_view="api.configuration_static_location_begin_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="ConfigurationStaticLocationBeginActionSchema",
        type_="configuration_static_location_action",
        id_field="id",
    )
    configuration_dynamic_location_actions = Relationship(
        attribute="configuration_dynamic_location_begin_actions",
        related_view="api.configuration_dynamic_location_begin_action_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="ConfigurationDynamicLocationBeginActionSchema",
        type_="configuration_dynamic_location_action",
        id_field="id",
    )
    created_by = Relationship(
        self_view="api.user_list",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        dump_only=True,
    )
    updated_by = Relationship(
        self_view="api.user_list",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        dump_only=True,
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


class ConfigurationSchemaForOnlyId(Schema):
    class Meta:
        type_ = "configuration"
        self_view = "api.configuration_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.configuration_list"

    id = fields.Integer(as_string=True)
