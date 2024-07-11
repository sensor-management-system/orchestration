# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class DeviceCalibrationAttachmentSchema(Schema):
    """
    This class create a schema for a device calibration attachment.
    It uses the  marshmallow-jsonapi library that fit
    the JSONAPI 1.0 specification and provides Flask integration.
    """

    class Meta:
        type_ = "device_calibration_attachment"
        self_view = "api.device_calibration_attachment_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.device_calibration_attachment_list"

    id = fields.Integer(as_string=True)
    action = Relationship(
        related_view="api.device_calibration_action_detail",
        related_view_kwargs={"id": "<action_id>"},
        include_resource_linkage=True,
        schema="DeviceCalibrationActionSchema",
        type_="device_calibration_action",
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
