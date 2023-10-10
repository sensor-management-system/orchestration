# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for configuration parameter value change actions."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.configuration_parameter_value_change_action_schema import (
    ConfigurationParameterValueChangeActionSchema,
)

schema_mapper = MarshmallowJsonApiToOpenApiMapper(
    ConfigurationParameterValueChangeActionSchema
)

paths = {
    "/configuration-parameter-value-change-actions": {
        "get": {
            "tags": ["Configuration parameter value change actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
            ],
            "responses": {
                "200": {
                    "description": "List of configuration parameter value change actions",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                },
            },
            "description": "Retrieve the list of configuration parameter value change actions",
            "operationId": "RetriececollectionofConfigurationParameterValueChangeActionobjects",
        },
        "post": {
            "tags": ["Configuration parameter value change actions"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created configuration parameter value change action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreateConfigurationParameterValuechangeAction",
        },
    },
    "/configuration-parameter-value-change-actions/{configuration_parameter_value_change_action_id}": {
        "get": {
            "tags": ["Configuration parameter value change actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {
                    "$ref": "#/components/parameters/configuration_parameter_value_change_action_id"
                },
            ],
            "responses": {
                "200": {
                    "description": "Instance of a configuration parameter value change action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a single configuration parameter value change action",
            "operationId": "RetrieveConfigurationParameterValueChangeActioninstance",
        },
        "patch": {
            "tags": ["Configuration parameter value change actions"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/configuration_parameter_value_change_action_id"
                },
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "ConfigurationParameterValueChangeAction attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated configuration parameter value change action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update ConfigurationParameterValueChangeAction attributes",
            "operationId": "UpdateConfigurationParameterValueChangeAction",
        },
        "delete": {
            "tags": ["Configuration parameter value change actions"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/configuration_parameter_value_change_action_id"
                }
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeleteConfigurationParameterValueChangeAction",
        },
    },
}

components = {
    "parameters": {
        "configuration_parameter_value_change_action_id": {
            "name": "configuration_parameter_value_change_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
