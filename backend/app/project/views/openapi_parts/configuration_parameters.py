# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for configuration parameters."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.configuration_parameter_schema import ConfigurationParameterSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(ConfigurationParameterSchema)

paths = {
    "/configuration-parameters": {
        "get": {
            "tags": ["Configuration parameters"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of configuration parameters",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                },
            },
            "description": "Retrieve the list of configuration parameters",
            "operationId": "RetriececollectionofConfigurationParameterobjects",
        },
        "post": {
            "tags": ["Configuration parameters"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created configuration parameter",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreateConfigurationParameter",
        },
    },
    "/configuration-parameters/{configuration_parameter_id}": {
        "get": {
            "tags": ["Configuration parameters"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/configuration_parameter_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a configuration parameter",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a single configuration parameter",
            "operationId": "RetrieveConfigurationParameterinstance",
        },
        "patch": {
            "tags": ["Configuration parameters"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_parameter_id"},
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "ConfigurationParameter attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated configuration parameter",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update ConfigurationParameter attributes",
            "operationId": "UpdateConfigurationParameter",
        },
        "delete": {
            "tags": ["Configuration parameters"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_parameter_id"}
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeleteConfigurationParameter",
        },
    },
}

components = {
    "parameters": {
        "configuration_parameter_id": {
            "name": "configuration_parameter_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
