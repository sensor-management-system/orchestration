# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for the configuration endpoints."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.configuration_schema import ConfigurationSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(ConfigurationSchema)

paths = {
    "/configurations": {
        "get": {
            "tags": ["Configurations"],
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
                    "description": "List of configurations",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve Configuration from configuration",
            "operationId": "RetrieveacollectionofConfigurationobjects_0",
        },
        "post": {
            "tags": ["Configurations"],
            "description": "create a Configuration",
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created configuration",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "operationId": "CreateConfiguration_0",
        },
    },
    "/sites/{site_id}/configurations": {
        "get": {
            "tags": ["Configurations"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
                {"$ref": "#/components/parameters/site_id"},
                {"$ref": "#/components/parameters/filter"},
                {"$ref": "#/components/parameters/hide_archived"},
            ],
            "responses": {
                "200": {
                    "description": "List of configurations for the given site",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve the configurations for a specific site.",
            "operationId": "RetrieveacollectionofSite_0",
        },
    },
    "/configurations/{configuration_id}": {
        "get": {
            "tags": ["Configurations"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/configuration_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a configuration",
                    "content": {
                        "application/vnd.api.json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Retrieve Configuration from configuration",
            "operationId": "RetrieveConfigurationinstance_0",
        },
        "patch": {
            "tags": ["Configurations"],
            "parameters": [{"$ref": "#/components/parameters/configuration_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Configuration attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated configuration",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Update Configuration attributes",
            "operationId": "UpdateConfiguration_0",
        },
        "delete": {
            "tags": ["Configurations"],
            "parameters": [{"$ref": "#/components/parameters/configuration_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteConfigurationfromconfiguration_0",
        },
    },
    "/configurations/{configuration_id}/sensorml": {
        "get": {
            "tags": ["Configurations"],
            "parameters": [{"$ref": "#/components/parameters/configuration_id"}],
            "responses": {
                "200": {
                    "description": "SensorML response for the configuration",
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
            "description": "Retrieve Configuration sensorML",
            "operationId": "RetrieveConfigurationSensorML",
        },
    },
    "/configurations/{configuration_id}/archive": {
        "post": {
            "tags": ["Configurations"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_id"},
            ],
            "responses": {
                "204": {"description": "Configuration was archived succesfully."},
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
            "description": "Archive a configuration.",
            "operationId": "ArchiveConfiguration",
        }
    },
    "/configurations/{configuration_id}/restore": {
        "post": {
            "tags": ["Configurations"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_id"},
            ],
            "responses": {
                "204": {"description": "Restoring of the configuration was succesful."},
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
            "description": "Restore an archived configuration.",
            "operationId": "RestoreConfiguration",
        }
    },
}
components = {
    "parameters": {
        "configuration_id": {
            "name": "configuration_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
