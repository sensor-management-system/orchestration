# SPDX-FileCopyrightText: 2021 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Schemas for the mount action classes."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class PlatformMountActionSchema(Schema):
    """
    This class creates a schema for a platform_mount_action.

    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        """Meta class for the PlatformMountActionSchema."""

        type_ = "platform_mount_action"
        self_view = "api.platform_mount_action_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    begin_date = fields.DateTime(required=True)
    end_date = fields.DateTime(allow_none=True)
    begin_description = fields.Str(allow_none=True)
    end_description = fields.Str(allow_none=True)
    offset_x = fields.Float(allow_none=True)
    offset_y = fields.Float(allow_none=True)
    offset_z = fields.Float(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    platform_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    platform = Relationship(
        attribute="platform",
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<platform_id>"},
        include_resource_linkage=True,
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    parent_platform_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    parent_platform = Relationship(
        attribute="parent_platform",
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<parent_platform_id>"},
        include_resource_linkage=True,
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    configuration_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    configuration = Relationship(
        attribute="configuration",
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        schema="ConfigurationSchema",
        type_="configuration",
        id_field="id",
    )
    begin_contact = Relationship(
        attribute="begin_contact",
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<begin_contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    end_contact = Relationship(
        attribute="end_contact",
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<end_contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
        allow_none=True,
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


class DeviceMountActionSchema(Schema):
    """
    This class creates a schema for a device_mount_action.

    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        """Meta class for the DeviceMountActionSchema."""

        type_ = "device_mount_action"
        self_view = "api.device_mount_action_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    begin_date = fields.DateTime(required=True)
    end_date = fields.DateTime(allow_none=True)
    begin_description = fields.Str(allow_none=True)
    end_description = fields.Str(allow_none=True)
    offset_x = fields.Float(allow_none=True)
    offset_y = fields.Float(allow_none=True)
    offset_z = fields.Float(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    device_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    device = Relationship(
        attribute="device",
        related_view="api.device_detail",
        related_view_kwargs={"id": "<device_id>"},
        include_resource_linkage=True,
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )
    parent_platform_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    parent_platform = Relationship(
        attribute="parent_platform",
        related_view="api.platform_detail",
        related_view_kwargs={"id": "<parent_platform_id>"},
        include_resource_linkage=True,
        schema="PlatformSchema",
        type_="platform",
        id_field="id",
    )
    parent_device_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    parent_device = Relationship(
        attribute="parent_device",
        related_view="api.device_detail",
        related_view_kwargs={"id": "<parent_device_id>"},
        include_resource_linkage=True,
        schema="DeviceSchema",
        type_="device",
        id_field="id",
    )
    configuration_id = fields.Integer(dump_only=True, load_only=True, as_string=True)
    configuration = Relationship(
        attribute="configuration",
        related_view="api.configuration_detail",
        related_view_kwargs={"id": "<configuration_id>"},
        include_resource_linkage=True,
        schema="ConfigurationSchema",
        type_="configuration",
        id_field="id",
    )
    begin_contact = Relationship(
        attribute="begin_contact",
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<begin_contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
    end_contact = Relationship(
        attribute="end_contact",
        related_view="api.contact_detail",
        related_view_kwargs={"id": "<end_contact_id>"},
        include_resource_linkage=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
        allow_none=True,
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
