from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class PlatformSchema(Schema):
    class Meta:
        type_ = 'platform'
        self_view = 'platform_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'platform_list'

    id = fields.Integer(as_string=True, dump_only=True)
    description = fields.Str(required=True, load_only=True)
    shortName = fields.Str(required=True, reload_only=True)
    longName = fields.Str(load_only=True)
    manufacturer = fields.Str(required=True, load_only=True)
    type = fields.Str(required=True, load_only=True)
    platformType = fields.Str(required=True, load_only=True)
    website = fields.Str(load_only=True)
    configurationDate = fields.Date()
    inventoryNumber = fields.Integer(as_string=True)
    platformURN = fields.Function(lambda obj: "{}_{}".format(
        obj.platformType.upper(), obj.shortName.upper()))
    devices = Relationship(self_view='platform_devices',
                           self_view_kwargs={'id': '<id>'},
                           related_view='devices_list',
                           related_view_kwargs={'id': '<id>'},
                           many=True,
                           schema='DeviceSchema',
                           type_='device')
