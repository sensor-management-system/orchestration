# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for the device endpoints."""
paths = {
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
components = {}
