from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class PlatformSoftwareUpdateActionSchema(Schema):
    class Meta:
        type_ = "platform_software_update_action"
        self_view = "api.platform_software_update_action_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.platform_software_update_action_list"

    id = fields.Integer(as_string=True)
    software_type_name = fields.Str(allow_none=False)
    software_type_uri = fields.Str(allow_none=True)
    version = fields.Str(allow_none=True)
    repository_url = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    update_date = fields.DateTime(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    platform = Relationship(
        self_view="api.platform_software_update_action_platform",
        self_view_kwargs={"id": "<id>"},
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<platform_id>"},
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )

    contact = Relationship(
        self_view="api.platform_software_update_action_contact",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<id>"},
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    created_by = Relationship(
        self_view="api.platform_software_update_action_created_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        type_="user",
        id_field="id",
    )
    updated_by = Relationship(
        self_view="api.platform_software_update_action_updated_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        type_="user",
        id_field="id",
    )


class DeviceSoftwareUpdateActionSchema(Schema):
    class Meta:
        type_ = "device_software_update_action"
        self_view = "api.device_software_update_action_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.device_software_update_action_list"

    id = fields.Integer(as_string=True)
    software_type_name = fields.Str(allow_none=False)
    software_type_uri = fields.Str(allow_none=True)
    version = fields.Str(allow_none=True)
    repository_url = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    update_date = fields.DateTime(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    device = Relationship(
        self_view="api.device_software_update_action_device",
        self_view_kwargs={"id": "<id>"},
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )

    contact = Relationship(
        self_view="api.device_software_update_action_contact",
        self_view_kwargs={"id": "<id>"},
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<id>"},
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    created_by = Relationship(
        self_view="api.device_software_update_action_created_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        type_="user",
        id_field="id",
    )
    updated_by = Relationship(
        self_view="api.device_software_update_action_updated_user",
        self_view_kwargs={"id": "<id>"},
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        type_="user",
        id_field="id",
    )
