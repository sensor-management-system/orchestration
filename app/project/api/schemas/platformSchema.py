from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class PlatformSchema(Schema):
    class Meta:
        type_ = 'platform'
        self_view = 'platform_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'platform_list'

    id = fields.Integer(as_string=True, dump_only=True)
    description = fields.Str(allow_none=True)
    shortName = fields.Str(required=True)
    longName = fields.Str(allow_none=True)
    manufacturer = fields.Str(allow_none=True)
    type = fields.Str(required=True)
    platformType = fields.Str(allow_none=True)
    src = fields.Str(allow_none=True)
    configurationDate = fields.Date(allow_none=True)
    inventoryNumber = fields.Integer(allow_none=True)
    urn = fields.Function(lambda obj: "[{}]_[{}]".format(
        obj.type.upper(), obj.shortName.upper()))
    devices = Relationship(self_view='platform_devices',
                           self_view_kwargs={'id': '<id>'},
                           related_view='devices_list',
                           related_view_kwargs={'id': '<id>'},
                           many=True,
                           schema='DeviceSchema',
                           type_='device')
