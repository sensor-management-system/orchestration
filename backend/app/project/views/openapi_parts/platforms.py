# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""External openapi spec file for the platform endpoints."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.platform_schema import PlatformSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(PlatformSchema)

paths = {
    "/platforms": {
        "get": {
            "tags": ["Platforms"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
                {"$ref": "#/components/parameters/filter"},
                {"$ref": "#/components/parameters/hide_archived"},
            ],
            "responses": {
                "200": {
                    "description": "List of platforms",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                },
                "400": {
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {"$ref": "#/components/schemas/invalid_filters"}
                        }
                    },
                    "description": "Invalid filter parameter.",
                },
            },
            "description": "Retrieve Platform",
            "operationId": "RetrieveacollectionofPlatformobjects_0",
        },
        "post": {
            "tags": ["Platforms"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created platform",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
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
                "409": {
                    "description": "Conflict on performing the operation",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {"$ref": "#/components/schemas/conflict"}
                        }
                    },
                },
            },
            "operationId": "CreatePlatform_0",
            "parameters": [],
        },
    },
    "/platforms/{platform_id}": {
        "get": {
            "tags": ["Platforms"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/platform_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a platform",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve Platform from platform",
            "operationId": "RetrievePlatforminstance_0",
        },
        "patch": {
            "tags": ["Platforms"],
            "parameters": [{"$ref": "#/components/parameters/platform_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Platform attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated platform",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
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
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update Platform attributes",
            "operationId": "UpdatePlatform_0",
        },
        "delete": {
            "tags": ["Platforms"],
            "parameters": [{"$ref": "#/components/parameters/platform_id"}],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
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
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeletePlatformfromplatform_3",
        },
    },
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
            "tags": ["Platforms"],
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
            "tags": ["Platforms"],
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
components = {
    "parameters": {
        "platform_id": {
            "name": "platform_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    }
}
