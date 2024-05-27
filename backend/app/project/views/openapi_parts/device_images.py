# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.device_image_schema import DeviceImageSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(DeviceImageSchema)

paths = {
    "/device-images": {
        "get": {
            "tags": ["Device images"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of device images",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve a list of device images",
            "operationId": "RetrievecollectionofDeviceImageobjects",
        },
        "post": {
            "tags": ["Device images"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created device image",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreateDeviceImage",
        },
    },
    "/device-images/{device_image_id}": {
        "get": {
            "tags": ["Device images"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/device_image_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a device image",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a single device image",
            "operationId": "RetrieveDeviceImageInstance",
        },
        "patch": {
            "tags": ["Device images"],
            "parameters": [
                {"$ref": "#/components/parameters/device_image_id"},
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "DeviceImage attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated device image",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update DeviceImage attributes",
            "operationId": "UpdateDeviceImage",
        },
        "delete": {
            "tags": ["Device images"],
            "parameters": [
                {"$ref": "#/components/parameters/device_image_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeleteDeviceImage",
        },
    },
}

components = {
    "parameters": {
        "device_image_id": {
            "name": "device_image_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
