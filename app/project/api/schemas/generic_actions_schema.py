from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class GenericPlatformActionSchema(Schema):
    """
    This class create a schema for a generic_platform_action.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

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
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    platform = Relationship(
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<platform_id>"},
        include_resource_linkage=True,
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )

    contact = Relationship(
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    created_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        id_field="id",
        dump_only=True,
    )
    updated_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        id_field="id",
        dump_only=True,
    )
    generic_platform_action_attachments = Relationship(
        related_view="api.generic_platform_action_attachment_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="GenericPlatformActionAttachmentSchema",
        type_="generic_platform_action_attachment",
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
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    device = Relationship(
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        include_resource_linkage=True,
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )

    contact = Relationship(
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    created_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        id_field="id",
        dump_only=True,
    )
    updated_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        id_field="id",
        dump_only=True,
    )
    generic_device_action_attachments = Relationship(
        related_view="api.generic_device_action_attachment_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="GenericDeviceActionAttachmentSchema",
        type_="generic_device_action_attachment",
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
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    configuration = Relationship(
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        schema="ConfigurationSchema",
        type_="configuration",
        id_field="id",
    )

    contact = Relationship(
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )

    created_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<created_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        dump_only=True,
    )

    updated_by = Relationship(
        related_view="api.user_detail",
        related_view_kwargs={"id": "<updated_by_id>"},
        include_resource_linkage=True,
        schema="UserSchema",
        type_="user",
        dump_only=True,
        dump_only=True,
    )
    generic_configuration_action_attachments = Relationship(
        related_view="api.generic_configuration_action_attachment_list",
        related_view_kwargs={"id": "<id>"},
        include_resource_linkage=True,
        many=True,
        schema="GenericConfigurationActionAttachmentSchema",
        type_="generic_configuration_action_attachment",
        id_field="id",
    )
