# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi specs for the device calibration actions."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.calibration_actions_schema import DeviceCalibrationActionSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(DeviceCalibrationActionSchema)

paths = {
    "/device-calibration-actions": {
        "get": {
            "tags": ["Device calibration actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {
                "200": {
                    "description": "List of device calibrations",
                    "content": {"application/vnd.api+json": schema_mapper.get_list()},
                },
            },
        },
        "post": {
            "tags": ["Device calibration actions"],
            "requestBody": {
                "content": {"application/vnd.api+json": schema_mapper.post()},
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created device calibration action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
    },
    "/device-calibration-actions/{device_calibration_action_id}": {
        "get": {
            "tags": ["Device calibration actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/device_calibration_action_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a device calibration action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "patch": {
            "tags": ["Device calibration actions"],
            "parameters": [
                {"$ref": "#/components/parameters/device_calibration_action_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Device calibration action attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated device calibration action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "delete": {
            "tags": ["Device calibration actions"],
            "parameters": [
                {"$ref": "#/components/parameters/device_calibration_action_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "parameters": {
        "device_calibration_action_id": {
            "name": "device_calibration_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    }
}
