# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for device parameter value change actions."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.device_parameter_value_change_action_schema import (
    DeviceParameterValueChangeActionSchema,
)

schema_mapper = MarshmallowJsonApiToOpenApiMapper(
    DeviceParameterValueChangeActionSchema
)

paths = {
    "/device-parameter-value-change-actions": {
        "get": {
            "tags": ["Device parameter value change actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of device parameter value change actions",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                },
            },
            "description": "Retrieve the list of device parameter value change actions",
            "operationId": "RetriececollectionofDeviceParameterValueChangeActionobjects",
        },
        "post": {
            "tags": ["Device parameter value change actions"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created device parameter value change action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreateDeviceParameterValuechangeAction",
        },
    },
    "/device-parameter-value-change-actions/{device_parameter_value_change_action_id}": {
        "get": {
            "tags": ["Device parameter value change actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {
                    "$ref": "#/components/parameters/device_parameter_value_change_action_id"
                },
            ],
            "responses": {
                "200": {
                    "description": "Instance of the device parameter value change action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a single device parameter value change action",
            "operationId": "RetrieveDeviceParameterValueChangeActioninstance",
        },
        "patch": {
            "tags": ["Device parameter value change actions"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/device_parameter_value_change_action_id"
                },
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "DeviceParameterValueChangeAction attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated device parameter value change action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update DeviceParameterValueChangeAction attributes",
            "operationId": "UpdateDeviceParameterValueChangeAction",
        },
        "delete": {
            "tags": ["Device parameter value change actions"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/device_parameter_value_change_action_id"
                }
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeleteDeviceParameterValueChangeAction",
        },
    },
}

components = {
    "parameters": {
        "device_parameter_value_change_action_id": {
            "name": "device_parameter_value_change_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
