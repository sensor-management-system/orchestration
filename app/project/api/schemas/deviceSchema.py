from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class DeviceSchema(Schema):
    """
    This class create a schema for a device. Every attribute in the
    schema going to expose through the api.
    DeviceSchema has an attribute named “deviceURN” that is the result
     of concatenation manufacturer, model,
    type and serialNumber.
    It uses library called marshmallow-jsonapi that fit the JSONAPI 1.0
    specification and provides Flask integration.

    """

    class Meta:
        type_ = 'device'
        self_view = 'devices_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    description = fields.Str(allow_none=True)
    short_name = fields.Str(allow_none=True)
    long_name = fields.Str(allow_none=True)
    manufacturer = fields.Str(required=True)
    serial_number = fields.Integer(as_string=True, required=True)
    type = fields.Str(required=True)
    model = fields.Str(required=True)
    dual_use = fields.Boolean()
    label = fields.Str(allow_none=True)
    inventory_number = fields.Integer()
    website = fields.Str(allow_none=True)
    configuration_date = fields.Date()
    persistent_identifier = fields.Integer()

    urn = fields.Function(lambda obj: "{}_{}_{}_{}".format(
        obj.manufacturer.upper(), obj.model.upper(),
        obj.type.upper(), obj.serial_number))

    platform = Relationship(attribute='platform',
                            self_view='device_platform',
                            self_view_kwargs={'id': '<id>'},
                            related_view='platform_detail',
                            related_view_kwargs={'device_id': '<id>'},
                            schema='PlatformSchema',
                            type_='platform')

    events = Relationship(attribute='events',
                          self_view='device_events',
                          self_view_kwargs={'id': '<id>'},
                          related_view='events_list',
                          related_view_kwargs={'device_id': '<id>'},
                          many=True,
                          schema='EventSchema',
                          type_='event',
                          id_field='event_id')

    contacts = Relationship(attribute='contacts',
                            self_view='device_contacts',
                            self_view_kwargs={'id': '<id>'},
                            related_view='contacts_list',
                            related_view_kwargs={'device_id': '<id>'},
                            many=True,
                            schema='ContactSchema',
                            type_='contact',
                            id_field='contact_id')

    properties = Relationship(attribute='properties',
                              self_view='device_properties',
                              self_view_kwargs={'id': '<id>'},
                              related_view='contacts_list',
                              related_view_kwargs={'device_id': '<id>'},
                              many=True,
                              schema='PropertiesSchema',
                              type_='properties',
                              id_field='properties_id')

    attachments = Relationship(attribute='attachments',
                               self_view='device_attachments',
                               self_view_kwargs={'id': '<id>'},
                               related_view='attachments_list',
                               related_view_kwargs={'device_id': '<id>'},
                               many=True,
                               schema='AttachmentSchema',
                               type_='Attachment',
                               id_field='attachment_id')

    customfields = Relationship(attribute='customfields',
                                self_view='device_customfields',
                                self_view_kwargs={'id': '<id>'},
                                related_view='customfields_list',
                                related_view_kwargs={'device_id': '<id>'},
                                many=True,
                                schema='CustomFieldSchema',
                                type_='CustomField',
                                id_field='customfield_id')
