from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class GenericPlatformActionSchema(Schema):
    class Meta:
        type_ = "generic_platform_action"
        self_view = "api.generic_platform_action_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.generic_platform_action_list"

    id = fields.Integer(as_string=True)
    description = fields.Str(allow_none=True)
    action_type_name = fields.Str(required=True)
    action_type_uri = fields.Str(allow_none=True)
    begin_date = fields.DateTime(required=True)
    end_date = fields.DateTime(allow_none=True)

    platform = Relationship(
        self_view="api.generic_platform_action_device",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<platform_id>"},
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )

    contact = Relationship(
        self_view="api.generic_platform_action_contact",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )


class GenericDeviceActionSchema(Schema):
    class Meta:
        type_ = "generic_device_action"
        self_view = "api.generic_device_action_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.generic_device_action_list"

    id = fields.Integer(as_string=True)
    description = fields.Str(allow_none=True)
    action_type_name = fields.Str(required=True)
    action_type_uri = fields.Str(allow_none=True)
    begin_date = fields.DateTime(required=True)
    end_date = fields.DateTime(allow_none=True)

    device = Relationship(
        self_view="api.generic_device_action_device",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )

    contact = Relationship(
        self_view="api.generic_device_action_contact",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )


class GenericConfigurationActionSchema(Schema):
    class Meta:
        type_ = "generic_configuration_action"
        self_view = "api.generic_configuration_action_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.generic_configuration_action_list"

    id = fields.Integer(as_string=True)
    description = fields.Str(allow_none=True)
    action_type_name = fields.Str(required=True)
    action_type_uri = fields.Str(allow_none=True)
    begin_date = fields.DateTime(required=True)
    end_date = fields.DateTime(allow_none=True)

    configuration = Relationship(
        self_view="api.generic_configuration_action_configuration",
        self_view_kwargs={"id": "<id>"},
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        schema="ConfigurationSchema",
        type_="configuration",
        id_field="id",
    )

    contact = Relationship(
        self_view="api.generic_configuration_action_contact",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
