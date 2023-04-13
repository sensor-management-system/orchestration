# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for device attachments."""

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
                "200": {"$ref": "#/components/responses/DeviceProperty_coll1"}
            },
            "description": "Retrieve DeviceProperty from device_property",
            "operationId": "RetrieveacollectionofDevicePropertyobjects_0",
        },
        "post": {
            "tags": ["Device properties"],
            "requestBody": {"$ref": "#/components/requestBodies/DeviceProperty_inst"},
            "responses": {
                "201": {"$ref": "#/components/responses/DeviceProperty_coll1"}
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
                "200": {"$ref": "#/components/responses/DeviceProperty_coll1"}
            },
            "description": "Retrieve DeviceProperty from device_property",
            "operationId": "RetrieveDevicePropertyinstance_0",
        },
        "patch": {
            "tags": ["Device properties"],
            "parameters": [{"$ref": "#/components/parameters/device_property_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/DeviceProperty"}
                    }
                },
                "description": "DeviceProperty attributes",
                "required": True,
            },
            "responses": {
                "200": {"$ref": "#/components/responses/DeviceProperty_coll1"}
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
    "requestBodies": {
        "DeviceProperty_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "measuring_range_min": {
                                                "type": "number",
                                            },
                                            "measuring_range_max": {
                                                "type": "number",
                                            },
                                            "failure_value": {
                                                "type": "number",
                                            },
                                            "accuracy": {
                                                "type": "number",
                                            },
                                            "resolution": {
                                                "type": "number",
                                            },
                                            "label": {"type": "string"},
                                            "unit_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "unit_name": {"type": "string"},
                                            "compartment_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "compartment_name": {"type": "string"},
                                            "property_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "property_name": {"type": "string"},
                                            "sampling_media_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "sampling_media_name": {"type": "string"},
                                            "resolution_unit_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "resolution_unit_name": {"type": "string"},
                                        },
                                    },
                                    "type": {"type": "string"},
                                },
                                "example": {
                                    "attributes": {
                                        "measuring_range_min": 0,
                                        "measuring_range_max": 0,
                                        "failure_value": 0,
                                        "accuracy": 0,
                                        "label": "",
                                        "unit_uri": "",
                                        "unit_name": "",
                                        "compartment_uri": "",
                                        "compartment_name": "",
                                        "property_uri": "",
                                        "property_name": "",
                                        "sampling_media_uri": "",
                                        "sampling_media_name": "",
                                        "resolution": 0,
                                        "resolution_unit_uri": "",
                                        "resolution_unit_name": "",
                                    },
                                    "type": "device_property",
                                    "relationships": {
                                        "device": {
                                            "data": {"type": "device", "id": "0"}
                                        }
                                    },
                                },
                            }
                        },
                        "description": "DeviceProperty post;",
                    }
                }
            }
        },
    },
    "responses": {
        "DeviceProperty_coll1": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "type": "string",
                                    },
                                    "type": {
                                        "type": "string",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "measuring_range_min": {
                                                "type": "number",
                                            },
                                            "measuring_range_max": {
                                                "type": "number",
                                            },
                                            "failure_value": {
                                                "type": "number",
                                            },
                                            "accuracy": {
                                                "type": "number",
                                            },
                                            "resolution": {
                                                "type": "number",
                                            },
                                            "label": {"type": "string"},
                                            "unit_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "unit_name": {"type": "string"},
                                            "compartment_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "compartment_name": {"type": "string"},
                                            "property_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "property_name": {"type": "string"},
                                            "sampling_media_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "sampling_media_name": {"type": "string"},
                                            "resolution_unit_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "resolution_unit_name": {"type": "string"},
                                            "created_at": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                            "updated_at": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                        },
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "properties": {
                                            "device": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {
                                                                "type": "string",
                                                            },
                                                            "type": {
                                                                "type": "string",
                                                                "default": "device",
                                                            },
                                                        },
                                                    }
                                                },
                                            },
                                            "created_by": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {
                                                                "type": "string",
                                                            },
                                                            "type": {
                                                                "type": "string",
                                                                "default": "user",
                                                            },
                                                        },
                                                    }
                                                },
                                            },
                                            "updated_by": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {
                                                                "type": "string",
                                                            },
                                                            "type": {
                                                                "type": "string",
                                                                "default": "user",
                                                            },
                                                        },
                                                    }
                                                },
                                            },
                                        },
                                    },
                                },
                                "example": {
                                    "attributes": {
                                        "measuring_range_min": 0,
                                        "measuring_range_max": 0,
                                        "failure_value": 0,
                                        "accuracy": 0,
                                        "label": "",
                                        "unit_uri": "",
                                        "unit_name": "",
                                        "compartment_uri": "",
                                        "compartment_name": "",
                                        "property_uri": "",
                                        "property_name": "",
                                        "sampling_media_uri": "",
                                        "sampling_media_name": "",
                                        "resolution": 0,
                                        "resolution_unit_uri": "",
                                        "resolution_unit_name": "",
                                        "created_at": "2023-01-01T00:00:00+00:00",
                                        "updated_at": "2023-01-01T00:00:00+00:00",
                                    },
                                    "type": "device_property",
                                    "id": "0",
                                    "relationships": {
                                        "device": {
                                            "data": {
                                                "id": "0",
                                                "type": "device",
                                            }
                                        },
                                        "created_by": {
                                            "data": {
                                                "id": "0",
                                                "type": "user",
                                            }
                                        },
                                        "updated_by": {
                                            "data": {
                                                "id": "0",
                                                "type": "user",
                                            }
                                        },
                                    },
                                },
                            }
                        },
                        "description": "DeviceProperty get;",
                    }
                }
            },
            "description": "Device Property",
        },
    },
    "schemas": {
        "DeviceProperty": {
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "attributes": {
                            "type": "object",
                            "properties": {
                                "measuring_range_min": {
                                    "type": "number",
                                },
                                "measuring_range_max": {
                                    "type": "number",
                                },
                                "failure_value": {
                                    "type": "number",
                                },
                                "accuracy": {
                                    "type": "number",
                                },
                                "resolution": {
                                    "type": "number",
                                },
                                "label": {"type": "string"},
                                "unit_uri": {"type": "string", "format": "uri"},
                                "unit_name": {"type": "string"},
                                "compartment_uri": {"type": "string", "format": "uri"},
                                "compartment_name": {"type": "string"},
                                "property_uri": {"type": "string", "format": "uri"},
                                "property_name": {"type": "string"},
                                "sampling_media_uri": {
                                    "type": "string",
                                    "format": "uri",
                                },
                                "sampling_media_name": {"type": "string"},
                                "resolution_unit_uri": {
                                    "type": "string",
                                    "format": "uri",
                                },
                                "resolution_unit_name": {"type": "string"},
                            },
                        },
                        "type": {"type": "string"},
                        "id": {"type": "string"},
                    },
                    "example": {
                        "attributes": {
                            "measuring_range_min": 0,
                            "measuring_range_max": 0,
                            "failure_value": 0,
                            "accuracy": 0,
                            "label": "",
                            "unit_uri": "",
                            "unit_name": "",
                            "compartment_uri": "",
                            "compartment_name": "",
                            "property_uri": "",
                            "property_name": "",
                            "sampling_media_uri": "",
                            "sampling_media_name": "",
                            "resolution": 0,
                            "resolution_unit_uri": "",
                            "resolution_unit_name": "",
                        },
                        "type": "device_property",
                        "id": "0",
                        "relationships": {
                            "device": {"data": {"type": "device", "id": "0"}}
                        },
                    },
                }
            },
            "description": "DeviceProperty post;",
        },
    },
    "parameters": {
        "device_property_id": {
            "name": "device_property_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
