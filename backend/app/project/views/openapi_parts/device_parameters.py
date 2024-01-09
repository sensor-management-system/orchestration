# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for device parameters."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.device_parameter_schema import DeviceParameterSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(DeviceParameterSchema)

paths = {
    "/device-parameters": {
        "get": {
            "tags": ["Device parameters"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of device parameters",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                },
            },
            "description": "Retrieve the list of device parameters",
            "operationId": "RetriececollectionofDeviceParameterobjects",
        },
        "post": {
            "tags": ["Device parameters"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created device parameter",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreateDeviceParameter",
        },
    },
    "/device-parameters/{device_parameter_id}": {
        "get": {
            "tags": ["Device parameters"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/device_parameter_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a device parameter",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a single device parameter",
            "operationId": "RetrieveDeviceParameterinstance",
        },
        "patch": {
            "tags": ["Device parameters"],
            "parameters": [
                {"$ref": "#/components/parameters/device_parameter_id"},
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "DeviceParameter attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated device parameter",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update DeviceParameter attributes",
            "operationId": "UpdateDeviceParameter",
        },
        "delete": {
            "tags": ["Device parameters"],
            "parameters": [{"$ref": "#/components/parameters/device_parameter_id"}],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeleteDeviceParameter",
        },
    },
}

components = {
    "parameters": {
        "device_parameter_id": {
            "name": "device_parameter_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
