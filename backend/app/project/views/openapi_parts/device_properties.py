# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""External openapi spec file for device properties."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.device_property_schema import DevicePropertySchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(DevicePropertySchema)

paths = {
    "/device-properties": {
        "get": {
            "tags": ["Device properties"],
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
                    "description": "List of device properties",
                    "content": {"application/vnd.api+json": schema_mapper.get_list()},
                }
            },
            "description": "Retrieve DeviceProperty from device_property",
            "operationId": "RetrieveacollectionofDevicePropertyobjects_0",
        },
        "post": {
            "tags": ["Device properties"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created device property",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "operationId": "CreateDeviceProperty_0",
        },
    },
    "/device-properties/{device_property_id}": {
        "get": {
            "tags": ["Device properties"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/device_property_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of device property",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve DeviceProperty from device_property",
            "operationId": "RetrieveDevicePropertyinstance_0",
        },
        "patch": {
            "tags": ["Device properties"],
            "parameters": [{"$ref": "#/components/parameters/device_property_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "DeviceProperty attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated device property",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Update DeviceProperty attributes",
            "operationId": "UpdateDeviceProperty_0",
        },
        "delete": {
            "tags": [
                "Device properties",
            ],
            "parameters": [{"$ref": "#/components/parameters/device_property_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteDevicePropertyfromdeviceproperty_1",
        },
    },
}

components = {
    "parameters": {
        "device_property_id": {
            "name": "device_property_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
