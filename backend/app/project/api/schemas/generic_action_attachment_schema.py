# SPDX-FileCopyrightText: 2021 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Schema classes for generic action attachments."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class GenericDeviceActionAttachmentSchema(Schema):
    """
    This class create a schema for a generic_device_action_attachment.

    It uses the  marshmallow-jsonapi library that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        """Meta class for GenericDeviceActionAttachmentSchema."""

        type_ = "generic_device_action_attachment"
        self_view = "api.generic_device_action_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.generic_device_action_attachment_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        related_view="api.generic_device_action_detail",
        related_view_kwargs={"id": "<action_id>"},
        include_resource_linkage=True,
        schema="GenericDeviceActionSchema",
        type_="generic_device_action",
        id_field="id",
    )
    attachment = Relationship(
        related_view="api.device_attachment_detail",
        related_view_kwargs={"id": "<attachment_id>"},
        include_resource_linkage=True,
        schema="DeviceAttachmentSchema",
        type_="device_attachment",
        id_field="id",
    )


class GenericPlatformActionAttachmentSchema(Schema):
    """
    This class create a schema for a generic_platform_action_attachment.

    It uses the  marshmallow-jsonapi library that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        """Meta class for GenericPlatformActionAttachmentSchema."""

        type_ = "generic_platform_action_attachment"
        self_view = "api.generic_platform_action_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.generic_platform_action_attachment_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        related_view="api.generic_platform_action_detail",
        related_view_kwargs={"id": "<action_id>"},
        include_resource_linkage=True,
        schema="GenericPlatformActionSchema",
        type_="generic_platform_action",
        id_field="id",
    )
    attachment = Relationship(
        related_view="api.platform_attachment_detail",
        related_view_kwargs={"id": "<attachment_id>"},
        include_resource_linkage=True,
        schema="PlatformAttachmentSchema",
        type_="platform_attachment",
        id_field="id",
    )


class GenericConfigurationActionAttachmentSchema(Schema):
    """
    This class create a schema for a generic_configuration_action_attachment.

    It uses the  marshmallow-jsonapi library that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        """Meta class for GenericConfigurationActionAttachmentSchema."""

        type_ = "generic_configuration_action_attachment"
        self_view = "api.generic_configuration_action_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.generic_configuration_action_attachment_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        related_view="api.generic_configuration_action_detail",
        related_view_kwargs={"id": "<action_id>"},
        include_resource_linkage=True,
        schema="GenericConfigurationActionSchema",
        type_="generic_configuration_action",
        id_field="id",
    )
    attachment = Relationship(
        related_view="api.configuration_attachment_detail",
        related_view_kwargs={"id": "<attachment_id>"},
        include_resource_linkage=True,
        schema="ConfigurationAttachmentSchema",
        type_="configuration_attachment",
        id_field="id",
    )
