from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from project.api.schemas.configuration_platform_schema import ConfigurationPlatformSchema

from project.api.schemas.device_schema import DeviceSchema
from project.api.schemas.platform_schema import PlatformSchema


class ConfigurationDeviceSchema(Schema):
    class Meta:
        type_ = "configuration_device"
        self_view = "api.configuration_device_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    offset_x = fields.Float()
    offset_y = fields.Float()
    offset_z = fields.Float()
    calibration_date = fields.DateTime()
    configuration_id = fields.Integer()
    firmware_version = fields.Str()

    configuration = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        type_="configuration",
        schema="ConfigurationSchema",
    )

    device = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        type_="device",
        schema="DeviceSchema",
    )

    parent_platform = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<parent_platform_id>"},
        type_="platform",
        schema="PlatformSchema",
    )

    @staticmethod
    def nested_dict_serializer(obj):
        """
        serialize the object to a nested dict.
        :param obj: a sensor object
        :return:
        """
        return ConfigurationDeviceToNestedDictSerializer().to_nested_dict(obj)


class ConfigurationDeviceToNestedDictSerializer:
    @staticmethod
    def to_nested_dict(obj):
        """Convert the object to a dict."""
        if obj is not None:
            return {
                "offset_x": obj.offset_x,
                "offset_y": obj.offset_y,
                "offset_z": obj.offset_z,
                "calibration_date": obj.calibration_date,
                "firmware_version": obj.firmware_version,
                "device": DeviceSchema().nested_dict_serializer(obj.device),
                "parent_platform": PlatformSchema().nested_dict_serializer(
                    obj.parent_platform),
            }