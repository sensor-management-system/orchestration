from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


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
    configuration_id = fields.Integer()

    configuration = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        type_="configuration",
    )

    device = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="device_detail",
        related_view_kwargs={"id": "<device_id>"},
        type_="device",
    )

    platform = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="platform_detail",
        related_view_kwargs={"id": "<platform_id>"},
        type_="platform",
    )
