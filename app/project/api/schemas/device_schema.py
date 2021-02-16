from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from project.api.schemas.attachment_schema import AttachmentSchema
from project.api.schemas.contact_schema import ContactSchema
from project.api.schemas.customfield_schema import CustomFieldSchema
from project.api.schemas.device_property_schema import (
    InnerDevicePropertySchema,
)


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
        type_ = "device"
        self_view = "api.device_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    description = fields.Str(allow_none=True)
    short_name = fields.Str(required=True)
    long_name = fields.Str(allow_none=True)
    serial_number = fields.Str(allow_none=True)
    manufacturer_uri = fields.Str(allow_none=True)
    manufacturer_name = fields.Str(allow_none=True)
    device_type_uri = fields.Str(allow_none=True)
    device_type_name = fields.Str(allow_none=True)
    status_uri = fields.Str(allow_none=True)
    status_name = fields.Str(allow_none=True)
    model = fields.Str(allow_none=True)
    dual_use = fields.Boolean(allow_none=True)
    inventory_number = fields.Str(allow_none=True)
    persistent_identifier = fields.Str(allow_none=True)
    website = fields.Str(allow_none=True)
    created_at = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(allow_none=True)
    created_by = Relationship(
        self_view="api.device_created_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        type_="user",
    )
    updated_by = Relationship(
        self_view="api.device_updated_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        type_="user",
    )
    customfields = fields.Nested(CustomFieldSchema, many=True, allow_none=True)
    events = Relationship(
        self_view="api.device_events",
        self_view_kwargs={"id": "<id>"},
        related_view="api.event_list",
        related_view_kwargs={"device_id": "<id>"},
        many=True,
        allow_none=True,
        schema="EventSchema",
        type_="event",
    )
    properties = fields.Nested(
        InnerDevicePropertySchema,
        many=True,
        allow_none=True,
        attribute="device_properties",
    )
    attachments = fields.Nested(
        AttachmentSchema, many=True, allow_none=True, attribute="device_attachments"
    )
    contacts = Relationship(
        attribute="contacts",
        self_view="api.device_contacts",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_list",
        related_view_kwargs={"device_id": "<id>"},
        many=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )

    @staticmethod
    def nested_dict_serializer(obj):
        """
        serialize the object to a nested dict.
        :param obj: a sensor object
        :return:
        """
        return DeviceToNestedDictSerializer().to_nested_dict(obj)


class DeviceToNestedDictSerializer:
    @staticmethod
    def to_nested_dict(device):
        """
         Convert to nested dict.
        :param device:
        :return:
        """
        if device is not None:
            return {
                "short_name": device.short_name,
                "long_name": device.long_name,
                "description": device.description,
                "serial_number": device.serial_number,
                "manufacturer_name": device.manufacturer_name,
                "manufacturer_uri": device.manufacturer_uri,
                "dual_use": device.dual_use,
                "model": device.model,
                "inventory_number": device.inventory_number,
                "persistent_identifier": device.persistent_identifier,
                "website": device.website,
                "device_type_name": device.device_type_name,
                "device_type_uri": device.device_type_uri,
                "status_name": device.status_name,
                "status_uri": device.status_uri,
                "attachments": [
                    AttachmentSchema().dict_serializer(a)
                    for a in device.device_attachments
                ],
                "contacts": [
                    ContactSchema().dict_serializer(c) for c in device.contacts
                ],
                "properties": [
                    InnerDevicePropertySchema().dict_serializer(p)
                    for p in device.device_properties
                ],
                "customfields": [
                    CustomFieldSchema.dict_serializer(c) for c in device.customfields
                ],
            }
