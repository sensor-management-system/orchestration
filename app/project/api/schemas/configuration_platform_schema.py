from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class ConfigurationPlatformSchema(Schema):
    class Meta:
        type_ = "configuration_platform"
        self_view = "configuration_platform_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    offset_x = fields.Float()
    offset_y = fields.Float()
    offset_z = fields.Float()
    configuration_id = fields.Integer()
    platform_id = fields.Integer()

    configuration = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        type_="configuration",
        schema="ConfigurationSchema",
    )
    parent_platform = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="platform_detail",
        related_view_kwargs={"id": "<parent_platform_id>"},
        type_="platform",
        schema="PlatformSchema",
    )
    platform = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="platform_detail",
        related_view_kwargs={"id": "<platform_id>"},
        type_="platform",
        schema="PlatformSchema",
    )
