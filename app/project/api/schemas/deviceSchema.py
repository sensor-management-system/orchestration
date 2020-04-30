from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class DeviceSchema(Schema):
    """
    This class create a schema for a device. Every attribute in the schema going to expose through the api.
    DeviceSchema has an attribute named “deviceURN” that is the result of concatenation manufacturer, model,
    type and serialNumber.
    It uses library called marshmallow-jsonapi that fit the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = 'device'
        self_view = 'devices_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    description = fields.Str(allow_none=True)
    shortName = fields.Str(allow_none=True)
    longName = fields.Str(allow_none=True)
    manufacture = fields.Str(required=True)
    serialNumber = fields.Integer(as_string=True, required=True)
    type = fields.Str(required=True)
    model = fields.Str(required=True)
    dualUse = fields.Str()
    label = fields.Str(allow_none=True)
    inventoryNumber = fields.Integer()
    website = fields.Str(allow_none=True)
    configurationDate = fields.Date()
    persistentIdentifier = fields.Integer()
    # deviceURN = fields.Function(lambda obj: "[{}]_[{}]_[{}]_[{}]".format(obj.manufacturer.upper(), obj.model.upper(),
    #                                                                     obj.type.upper(), obj.serialNumber.upper()))
    urn = fields.Function(lambda obj: "[{}]_[{}]_[{}]_[{}]".format(obj.manufacture.upper(), obj.model.upper(),
                                                                   obj.type.upper(), obj.serialNumber))
    platform = Relationship(attribute='platform',
                            self_view='device_platform',
                            self_view_kwargs={'id': '<id>'},
                            related_view='platform_detail',
                            related_view_kwargs={'device_id': '<id>'},
                            schema='PlatformSchema',
                            type_='platform')
