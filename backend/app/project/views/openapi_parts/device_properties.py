# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

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
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {
                    "name": "filter[measuring_range_min]",
                    "in": "query",
                    "required": False,
                    "description": "measuring_range_min attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[measuring_range_max]",
                    "in": "query",
                    "required": False,
                    "description": "measuring_range_max attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[failure_value]",
                    "in": "query",
                    "required": False,
                    "description": "failure_value attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[accuracy]",
                    "in": "query",
                    "required": False,
                    "description": "accuracy attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[label]",
                    "in": "query",
                    "required": False,
                    "description": "label attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[unit_uri]",
                    "in": "query",
                    "required": False,
                    "description": "unit_uri attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[unit_name]",
                    "in": "query",
                    "required": False,
                    "description": "unit_name attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[compartment_uri]",
                    "in": "query",
                    "required": False,
                    "description": "compartment_uri attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[compartment_name]",
                    "in": "query",
                    "required": False,
                    "description": "compartment_name attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[property_uri]",
                    "in": "query",
                    "required": False,
                    "description": "property_uri attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[property_name]",
                    "in": "query",
                    "required": False,
                    "description": "property_name attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[sampling_media_uri]",
                    "in": "query",
                    "required": False,
                    "description": "sampling_media_uri attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[sampling_media_name]",
                    "in": "query",
                    "required": False,
                    "description": "sampling_media_name attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[resolution]",
                    "in": "query",
                    "required": False,
                    "description": "resolution attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[resolution_unit_uri]",
                    "in": "query",
                    "required": False,
                    "description": "resolution_unit_uri attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[resolution_unit_name]",
                    "in": "query",
                    "required": False,
                    "description": "resolution_unit_name attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[device_id]",
                    "in": "query",
                    "required": False,
                    "description": "device_id attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {"$ref": "#/components/parameters/id"},
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
