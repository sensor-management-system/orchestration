from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship
from project.api.schemas.attachment_schema import AttachmentSchema
from project.api.schemas.customfield_schema import CustomFieldSchema
from project.api.schemas.event_schema import EventSchema
from project.api.schemas.device_property_schema import DevicePropertySchema


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
    short_name = fields.Str(required=True)
    long_name = fields.Str(allow_none=True)
    serial_number = fields.Str(allow_none=True)
    manufacturer_uri = fields.Str(allow_none=True)
    manufacturer_name = fields.Str(allow_none=True)
    model = fields.Str(allow_none=True)
    dual_use = fields.Boolean(allow_none=True)
    inventory_number = fields.Str(allow_none=True)
    persistent_identifier = fields.Str(allow_none=True)
    website = fields.Str(allow_none=True)
    created_at = fields.Date(allow_none=True)
    modified_at = fields.Date(allow_none=True)
    created_by = fields.Date(allow_none=True)
    created_by_id = fields.Date(allow_none=True)
    modified_by = fields.Date(allow_none=True)
    modified_by_id = fields.Date(allow_none=True)
    customfields = fields.Nested(CustomFieldSchema, many=True, allow_none=True)
    events = fields.Nested(EventSchema, many=True, allow_none=True)
    device_properties = fields.Nested(DevicePropertySchema, many=True, allow_none=True)
    device_attachments = fields.Nested(AttachmentSchema, many=True, allow_none=True)
    contacts = Relationship(attribute='contacts',
                            self_view='device_contacts',
                            self_view_kwargs={'id': '<id>'},
                            related_view='contacts_list',
                            related_view_kwargs={'device_id': '<id>'},
                            many=True,
                            schema='ContactSchema',
                            type_='contact',
                            id_field='id'
                            )
