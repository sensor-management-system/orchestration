"""Module for the device schema."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from ..schemas.attachment_schema import AttachmentSchema
from ..schemas.contact_schema import ContactSchema
from ..schemas.customfield_schema import InnerCustomFieldSchema
from ..schemas.device_property_schema import InnerDevicePropertySchema


class DeviceSchema(Schema):
    """
    This class create a schema for a device.

    Every attribute in the schema going to expose through the api.
    DeviceSchema has an attribute named “deviceURN” that is the result
     of concatenation manufacturer, model,
    type and serialNumber.
    It uses library called marshmallow-jsonapi that fit the JSONAPI 1.0
    specification and provides Flask integration.
    """

    class Meta:
        """Meta class for the DeviceSchema."""

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
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    created_by_id = fields.Str(dump_only=True)
    groups_ids = fields.Field(many=True, allow_none=True)
    is_private = fields.Boolean(required=True)
    is_internal = fields.Boolean(required=True)
    is_public = fields.Boolean(required=True)
    created_by = Relationship(
        attribute="created_by",
        self_view="api.device_created_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
    )
    updated_by = Relationship(
        self_view="api.device_updated_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
    )
    customfields = Relationship(
        related_view="api.device_customfields",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="CustomFieldSchema",
        type_="customfield",
        id_field="id",
    )
    events = Relationship(
        related_view="api.device_events",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="EventSchema",
        type_="event",
    )
    device_properties = Relationship(
        related_view="api.device_device_properties",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="DevicePropertySchema",
        type_="device_property",
        id_field="id",
    )
    device_attachments = Relationship(
        related_view="api.device_device_attachments",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        allow_none=True,
        schema="DeviceAttachmentSchema",
        type_="device_attachment",
        id_field="id",
    )
    contacts = Relationship(
        related_view="api.device_contacts",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    generic_device_actions = Relationship(
        related_view="api.device_generic_device_actions",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="GenericDeviceActionSchema",
        type_="generic_device_action",
        id_field="id",
    )
    device_mount_actions = Relationship(
        related_view="api.device_device_mount_actions",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="DeviceMountActionSchema",
        type_="device_mount_action",
        id_field="id",
    )
    device_unmount_actions = Relationship(
        related_view="api.device_device_unmount_actions",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="DeviceUnmountActionSchema",
        type_="device_unmount_action",
        id_field="id",
    )
    device_calibration_actions = Relationship(
        related_view="api.device_device_calibration_actions",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="DeviceCalibrationActionSchema",
        type_="device_calibration_action",
        id_field="id",
    )
    device_software_update_actions = Relationship(
        related_view="api.device_device_software_update_actions",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="DeviceSoftwareUpdateActionSchema",
        type_="device_software_update_action",
        id_field="id",
    )
    configuration_device = Relationship(
        self_view="api.device_configuration_device",
        self_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        schema="ConfigurationDeviceSchema",
        type_="configuration_device",
        id_field="id",
    )

    @staticmethod
    def nested_dict_serializer(obj):
        """
        Serialize the object to a nested dict.

        :param obj: a sensor object
        :return:
        """
        return DeviceToNestedDictSerializer().to_nested_dict(obj)


class DeviceToNestedDictSerializer:
    """
    Serializer to a nested dict.

    Intended to be used to export the device in a differnt way
    then the "normal" device serializer.

    This here for example can be used to create a nested dict, that
    may be flattened and then is used in a csv export.
    """

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
                    InnerCustomFieldSchema.dict_serializer(c)
                    for c in device.customfields
                ],
            }
