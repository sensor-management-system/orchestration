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
        self_view = 'device_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    description = fields.Str(allow_none=True)
    short_name = fields.Str(required=True, data_key="shortName")
    long_name = fields.Str(allow_none=True, data_key="longName")
    serial_number = fields.Str(allow_none=True, data_key="serialNumber")
    manufacturer_uri = fields.Str(allow_none=True, data_key="manufacturerUri")
    manufacturer_name = fields.Str(allow_none=True, data_key="manufacturerName")
    model = fields.Str(allow_none=True)
    dual_use = fields.Boolean(allow_none=True, data_key="dualUse")
    inventory_number = fields.Str(allow_none=True, data_key="inventoryNumber")
    persistent_identifier = fields.Str(allow_none=True, data_key="persistentIdentifier")
    website = fields.Url(allow_none=True)
    created_at = fields.DateTime(allow_none=True, data_key="createdAt")
    modified_at = fields.DateTime(allow_none=True, data_key="modifiedAt")
    # TODO: Those must be Users
    #created_by = fields.Date(allow_none=True, data_key="createdBy")
    #modified_by = fields.Date(allow_none=True, data_key="modifiedBy")
    created_by_id = fields.Integer(allow_none=True, data_key="createdById")
    modified_by_id = fields.Integer(allow_none=True, data_key="modifiedById")
    customfields = fields.Nested(CustomFieldSchema, many=True, allow_none=True)
    events = fields.Nested(EventSchema, many=True, allow_none=True)
    device_properties = fields.Nested(DevicePropertySchema, many=True, allow_none=True, data_key="deviceProperties")
    device_attachments = fields.Nested(AttachmentSchema, many=True, allow_none=True, data_key="attachments")
    contacts = Relationship(attribute='contacts',
                            self_view='device_contacts',
                            self_view_kwargs={'id': '<id>'},
                            related_view='contact_list',
                            related_view_kwargs={'device_id': '<id>'},
                            many=True,
                            schema='ContactSchema',
                            type_='contact',
                            id_field='id'
                            )
