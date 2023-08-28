# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Part of the openapi for pids."""

paths = {
    "/pids": {
        "post": {
            "tags": ["Pids"],
            "requestBody": {"$ref": "#/components/requestBodies/Pid_post"},
            "responses": {
                "201": {"$ref": "#/components/responses/Pid_response"},
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
            "operationId": "CreatePid",
        },
    }
}

components = {
    "requestBodies": {
        "Pid_post": {
            "description": "Payload to ask the system to create a pid for a device, platform or configuration.",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "instrument_instance": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["device", "platform", "configuration"],
                                    },
                                    "id": {
                                        "type": "string",
                                    },
                                },
                            },
                        }
                    }
                }
            },
        }
    },
    "responses": {
        "Pid_response": {
            "description": "Result of the pid generation.",
            "content": {
                "application/vnd.api+json": {
                    "schema": {"properties": {"pid": {"type": "string"}}}
                }
            },
        }
    },
}
