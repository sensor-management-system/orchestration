# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi specs for the device property calibrations."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.calibration_actions_schema import DevicePropertyCalibrationSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(DevicePropertyCalibrationSchema)

paths = {
    "/device-property-calibrations": {
        "get": {
            "tags": ["Device property calibrations"],
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
                    "description": "List of device property calibrations",
                    "content": {"application/vnd.api+json": schema_mapper.get_list()},
                },
            },
        },
        "post": {
            "tags": ["Device property calibrations"],
            "requestBody": {
                "content": {"application/vnd.api+json": schema_mapper.post()},
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created device property calibration",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
    },
    "/device-property-calibrations/{device_property_calibration_id}": {
        "get": {
            "tags": ["Device property calibrations"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/device_property_calibration_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a device property calibration",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "patch": {
            "tags": ["Device property calibrations"],
            "parameters": [
                {"$ref": "#/components/parameters/device_property_calibration_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Device property calibration attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated device property calibration",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "delete": {
            "tags": ["Device property calibrations"],
            "parameters": [
                {"$ref": "#/components/parameters/device_property_calibration_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "parameters": {
        "device_property_calibration_id": {
            "name": "device_property_calibration_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    }
}
