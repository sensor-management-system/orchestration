from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship

from project.api.schemas.configuration_schema import ConfigurationSchema
from project.api.schemas.platform_schema import PlatformSchema


class ConfigurationPlatformSchema(Schema):

    class Meta:
        type_ = "configuration_platform"
        self_view = "configuration_platform_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True, dump_only=True)
    offset_x = fields.Float()
    offset_y = fields.Float()
    offset_z = fields.Float()
    #
    # configuration = fields.Nested(
    #     ConfigurationSchema
    # )
    parent_platform = fields.Nested(
        PlatformSchema, allow_none=True
    )
    platform = fields.Nested(
        PlatformSchema
    )
