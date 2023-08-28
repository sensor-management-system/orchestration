# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for the platform endpoints."""
paths = {
    "/platforms/{platform_id}/sensorml": {
        "get": {
            "tags": ["Platforms"],
            "parameters": [{"$ref": "#/components/parameters/platform_id"}],
            "responses": {
                "200": {
                    "description": "SensorML response for the platform",
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
            "description": "Retrieve Platform sensorML",
            "operationId": "RetrievePlatformSensorML",
        },
    },
    "/platforms/{platform_id}/archive": {
        "post": {
            "tags": ["Platform"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_id"},
            ],
            "responses": {
                "204": {"description": "Platform was archived succesfully."},
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
            "description": "Archive a platform.",
            "operationId": "ArchivePlatform",
        }
    },
    "/platforms/{platform_id}/restore": {
        "post": {
            "tags": ["Platform"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_id"},
            ],
            "responses": {
                "204": {"description": "Restoring of the platform was succesful."},
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
            "description": "Restore an archived platform.",
            "operationId": "RestorePlatform",
        }
    },
}
components = {}
