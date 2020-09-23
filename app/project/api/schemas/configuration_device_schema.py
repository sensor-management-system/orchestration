from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship

from project.api.schemas.platform_schema import PlatformSchema
from project.api.schemas.device_schema import DeviceSchema


class ConfigurationDeviceSchema(Schema):

    class Meta:
        type_ = "configuration_device"
        self_view = "configuration_device_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True, dump_only=True)
    offset_x = fields.Float()
    offset_y = fields.Float()
    offset_z = fields.Float()
    calibration_date = fields.DateTime()
    #
    # configuration = fields.Nested(
    #     ConfigurationSchema
    # )
    device = fields.Nested(
        DeviceSchema
    )
    platform = fields.Nested(
        PlatformSchema
    )
