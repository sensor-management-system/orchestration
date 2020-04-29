from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship

class DeviceSchema(Schema):
    class Meta:
        type_ = 'device'
        self_view = 'devices_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    description = fields.Str(required=True, load_only=True)
    shortName = fields.Str(required=True, load_only=True)
    longName = fields.Str(load_only=True)
    manufacturer = fields.Str(required=True, load_only=True)
    serialNumber = fields.Integer(as_string=True)
    type = fields.Str(required=True, load_only=True)
    model = fields.Str(required=True, load_only=True)
    dualUse = fields.Str(load_only=True)
    label = fields.Str(required=True, load_only=True)
    inventoryNumber = fields.Integer(as_string=True)
    website = fields.Str(load_only=True)
    configurationDate = fields.Date()
    persistentIdentifier = fields.Integer(as_string=True)
    deviceURN = fields.Function(lambda obj: "{}_{}_{}_{}".format(obj.manufacturer.upper(), obj.model.upper(),
                                                                 obj.type.upper(), obj.serialNumber.upper()))
    platform = Relationship(attribute='platform',
                         self_view='device_platform',
                         self_view_kwargs={'id': '<id>'},
                         related_view='platform_detail',
                         related_view_kwargs={'device_id': '<id>'},
                         schema='PlatformSchema',
                         type_='platform')