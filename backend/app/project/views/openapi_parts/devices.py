# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for the device endpoints."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.device_schema import DeviceSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(DeviceSchema)

paths = {
    "/devices": {
        "get": {
            "tags": ["Devices"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {"$ref": "#/components/parameters/created_at"},
                {"$ref": "#/components/parameters/updated_at"},
                {"$ref": "#/components/parameters/created_by_id"},
                {"$ref": "#/components/parameters/updated_by_id"},
                {"$ref": "#/components/parameters/description"},
                {"$ref": "#/components/parameters/short_name"},
                {"$ref": "#/components/parameters/long_name"},
                {"$ref": "#/components/parameters/serial_number"},
                {"$ref": "#/components/parameters/manufacturer_uri"},
                {"$ref": "#/components/parameters/manufacturer_name"},
                {"$ref": "#/components/parameters/dual_use"},
                {"$ref": "#/components/parameters/model"},
                {"$ref": "#/components/parameters/inventory_number"},
                {"$ref": "#/components/parameters/persistent_identifier"},
                {"$ref": "#/components/parameters/website"},
                {"$ref": "#/components/parameters/device_type_uri"},
                {"$ref": "#/components/parameters/device_type_name"},
                {"$ref": "#/components/parameters/status_uri"},
                {"$ref": "#/components/parameters/status_name"},
                {"$ref": "#/components/parameters/id"},
                {"$ref": "#/components/parameters/filter"},
                {"$ref": "#/components/parameters/hide_archived"},
            ],
            "responses": {
                "200": {
                    "description": "List of devices",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve Device from device",
            "operationId": "RetrieveacollectionofDeviceobjects_0",
        },
        "post": {
            "tags": ["Devices"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created device",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "operationId": "CreateDevice_0",
            "parameters": [],
        },
    },
    "/devices/{device_id}": {
        "get": {
            "tags": ["Devices"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/device_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a device",
                    "content": {
                        "application/vnd.api.json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Retrieve Device from device",
            "operationId": "RetrieveDeviceinstance_0",
        },
        "patch": {
            "tags": ["Devices"],
            "parameters": [{"$ref": "#/components/parameters/device_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Device attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated device",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Update Device attributes",
            "operationId": "UpdateDevice_0",
        },
        "delete": {
            "tags": ["Devices"],
            "parameters": [{"$ref": "#/components/parameters/device_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteDevicefromdevice_3",
        },
    },
    "/devices/{device_id}/sensorml": {
        "get": {
            "tags": ["Devices"],
            "parameters": [{"$ref": "#/components/parameters/device_id"}],
            "responses": {
                "200": {
                    "description": "SensorML response for the device",
                    "content": {"application/xml": {}},
                },
                "401": {
                    "description": "Authentification required.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/authentification_required"
                            }
                        }
                    },
                },
            },
            "description": "Retrieve Device sensorML",
            "operationId": "RetrieveDeviceSensorML",
        },
    },
    "/devices/{device_id}/archive": {
        "post": {
            "tags": ["Devices"],
            "parameters": [
                {"$ref": "#/components/parameters/device_id"},
            ],
            "responses": {
                "204": {"description": "Device was archived succesfully."},
                "401": {
                    "description": "Authentification required.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/authentification_required"
                            }
                        }
                    },
                },
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
                "409": {
                    "description": "Conflict on performing the operation",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {"$ref": "#/components/schemas/conflict"}
                        }
                    },
                },
            },
            "description": "Archive a device.",
            "operationId": "ArchiveDevice",
        }
    },
    "/devices/{device_id}/restore": {
        "post": {
            "tags": ["Devices"],
            "parameters": [
                {"$ref": "#/components/parameters/device_id"},
            ],
            "responses": {
                "204": {"description": "Restoring of the device was succesful."},
                "401": {
                    "description": "Authentification required.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/authentification_required"
                            }
                        }
                    },
                },
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Restore an archived device.",
            "operationId": "RestoreDevice",
        }
    },
}
components = {
    "parameters": {
        "device_id": {
            "name": "device_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string", "default": "0"},
        }
    }
}
