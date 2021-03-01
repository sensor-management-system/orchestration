# from marshmallow_jsonapi import fields
# from marshmallow_jsonapi.flask import Relationship, Schema
#
#
# class PlatformMountActionSchema(Schema):
#     class Meta:
#         type_ = "platform_mount_action"
#         self_view = "api.platform_mount_action_detail"
#         self_view_kwargs = {"id": "<id>"}
#
#     id = fields.Integer(as_string=True)
#     begin_date = fields.DateTime(allow_none=False)
#     description = fields.Str(allow_none=True)
#     offset_x = fields.Float(allow_none=True)
#     offset_y = fields.Float(allow_none=True)
#     offset_z = fields.Float(allow_none=True)
#     platform = Relationship(
#         attribute="platforms",
#         self_view="api.platform_mount_action_platform",
#         self_view_kwargs={"id": "<id>"},
#         related_view="api.platform_list",
#         related_view_kwargs={"contact_id": "<id>"},
#         schema="PlatformSchema",
#         type_="platform",
#         id_field="id",
#     )
#     parent_platform = Relationship(
#         attribute="platforms",
#         self_view="api.platform_mount_action_parent_platform",
#         self_view_kwargs={"id": "<id>"},
#         related_view="api.platform_list",
#         related_view_kwargs={"contact_id": "<id>"},
#         schema="PlatformSchema",
#         type_="platform",
#         id_field="id",
#     )
#     configuration = Relationship(
#         attribute="configurations",
#         self_view="api.platform_mount_action_configuration",
#         self_view_kwargs={"id": "<id>"},
#         related_view="api.configuration_list",
#         related_view_kwargs={"contact_id": "<id>"},
#         schema="ConfigurationSchema",
#         type_="configuration",
#         id_field="id",
#     )
#     contacts = Relationship(
#         attribute="contacts",
#         self_view="api.platform_mount_action_contacts",
#         self_view_kwargs={"id": "<id>"},
#         related_view="api.contact_list",
#         related_view_kwargs={"device_id": "<id>"},
#         many=True,
#         schema="ContactSchema",
#         type_="contact",
#         id_field="id",
#     )
#
#
# class DeviceMountActionSchema(Schema):
#     class Meta:
#         type_ = "device_mount_action"
#         self_view = "api.platform_mount_action_detail"
#         self_view_kwargs = {"id": "<id>"}
#
#     id = fields.Integer(as_string=True)
#     begin_date = fields.DateTime(allow_none=False)
#     description = fields.Str(allow_none=True)
#     offset_x = fields.Float(allow_none=True)
#     offset_y = fields.Float(allow_none=True)
#     offset_z = fields.Float(allow_none=True)
#     device = Relationship(
#         attribute="devices",
#         self_view="api.contact_devices",
#         self_view_kwargs={"id": "<id>"},
#         related_view="api.device_list",
#         related_view_kwargs={"contact_id": "<id>"},
#         many=True,
#         schema="DeviceSchema",
#         type_="device",
#         id_field="id",
#     )
#     parent_platform = Relationship(
#         attribute="platforms",
#         self_view="api.contact_platforms",
#         self_view_kwargs={"id": "<id>"},
#         related_view="api.platform_list",
#         related_view_kwargs={"contact_id": "<id>"},
#         schema="PlatformSchema",
#         type_="platform",
#         id_field="id",
#     )
#     configuration = Relationship(
#         attribute="configurations",
#         self_view="api.contact_configurations",
#         self_view_kwargs={"id": "<id>"},
#         related_view="api.configuration_list",
#         related_view_kwargs={"contact_id": "<id>"},
#         schema="ConfigurationSchema",
#         type_="configuration",
#         id_field="id",
#     )
#     contacts = Relationship(
#         attribute="contacts",
#         self_view="api.device_contacts",
#         self_view_kwargs={"id": "<id>"},
#         related_view="api.contact_list",
#         related_view_kwargs={"device_id": "<id>"},
#         many=True,
#         schema="ContactSchema",
#         type_="contact",
#         id_field="id",
#     )
