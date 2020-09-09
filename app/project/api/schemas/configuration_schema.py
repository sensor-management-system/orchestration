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

    longitude_src_device_property = fields.Nested(
        DevicePropertySchema, allow_none=True
    )
    latitude_src_device_property = fields.Nested(
        DevicePropertySchema, allow_none=True
    )
    elevation_src_device_property = fields.Nested(
        DevicePropertySchema, allow_none=True
    )

    contacts = fields.Nested(
        ContactSchema, many=True, allow_none=True,
    )

    configuration_platforms = fields.Nested(
        "ConfigurationPlatformSchema", many=True, allow_none=True
    )

    configuration_devices = fields.Nested(
        "ConfigurationDeviceSchema", many=True, allow_none=True
    )
