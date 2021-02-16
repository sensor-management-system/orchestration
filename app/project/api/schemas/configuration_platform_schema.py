from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from project.api.schemas.platform_schema import PlatformSchema


class ConfigurationPlatformSchema(Schema):
    class Meta:
        type_ = "configuration_platform"
        self_view = "api.configuration_platform_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    offset_x = fields.Float()
    offset_y = fields.Float()
    offset_z = fields.Float()
    configuration_id = fields.Integer()
    platform_id = fields.Integer()

    configuration = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        type_="configuration",
        schema="ConfigurationSchema",
    )
    parent_platform = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<parent_platform_id>"},
        type_="platform",
        schema="PlatformSchema",
    )
    platform = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<platform_id>"},
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
        return ConfigurationPlatformToNestedDictSerializer().to_nested_dict(obj)


class ConfigurationPlatformToNestedDictSerializer:
    @staticmethod
    def to_nested_dict(obj):
        """Convert the object to a dict."""
        if obj is not None:
            return {
                "offset_x": obj.offset_x,
                "offset_y": obj.offset_y,
                "offset_z": obj.offset_z,
                "platform": PlatformSchema().nested_dict_serializer(obj.platform),
                "parent_platform": PlatformSchema().nested_dict_serializer(
                    obj.parent_platform),
            }