# SPDX-FileCopyrightText: 2022 - 2023
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Openapi parts for configuration custom fields."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.configuration_customfield_schema import (
    ConfigurationCustomFieldSchema,
)

schema_mapper = MarshmallowJsonApiToOpenApiMapper(ConfigurationCustomFieldSchema)

paths = {
    "/configuration-customfields": {
        "get": {
            "tags": ["Configuration custom fields"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {
                    "name": "filter[key]",
                    "in": "query",
                    "required": False,
                    "description": "key attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[value]",
                    "in": "query",
                    "required": False,
                    "description": "value attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[configuration_id]",
                    "in": "query",
                    "required": False,
                    "description": "configuration_id attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {"$ref": "#/components/parameters/id"},
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {
                "200": {
                    "description": "List of configuration custom fields",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve a list of configuration custom fields",
            "operationId": "RetrieveacollectionofConfigurationCustomFieldobjects_0",
        },
        "post": {
            "tags": ["Configuration custom fields"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                }
            },
            "responses": {
                "201": {
                    "description": "Payload of the created configuration custom field",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "operationId": "CreateConfigurationCustomField_0",
            "parameters": [],
        },
    },
    "/configuration-customfields/{configuration_custom_field_id}": {
        "get": {
            "tags": ["Configuration custom fields"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/configuration_custom_field_id"},
            ],
            "responses": {
                "200": {
                    "description": "Request fulfilled, document follows",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Retrieve a configuration custom field",
            "operationId": "RetrieveConfigurationCustomFieldinstance_0",
        },
        "patch": {
            "tags": ["Configuration custom fields"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_custom_field_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "ConfigurationCustomField update payload",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated configuration custom field",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Update ConfigurationCustomField attributes",
            "operationId": "UpdateConfigurationCustomField_0",
        },
        "delete": {
            "tags": ["Configuration custom fields"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_custom_field_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteConfigurationCustomFieldfromcustomfield_0",
        },
    },
}

components = {
    "parameters": {
        "configuration_custom_field_id": {
            "name": "configuration_custom_field_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
