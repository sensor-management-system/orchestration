# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi specs for the generic configuration actions."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.generic_actions_schema import GenericConfigurationActionSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(GenericConfigurationActionSchema)

paths = {
    "/generic-configuration-actions": {
        "get": {
            "tags": ["Generic configuration actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {
                "200": {
                    "description": "List of generic configuration actions",
                    "content": {"application/vnd.api+json": schema_mapper.get_list()},
                },
            },
        },
        "post": {
            "tags": ["Generic configuration actions"],
            "requestBody": {
                "content": {"application/vnd.api+json": schema_mapper.post()},
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created generic configuration action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
    },
    "/generic-configuration-actions/{generic_configuration_action_id}": {
        "get": {
            "tags": ["Generic configuration actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/generic_configuration_action_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a generic configuration action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "patch": {
            "tags": ["Generic configuration actions"],
            "parameters": [
                {"$ref": "#/components/parameters/generic_configuration_action_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Generic configuration action attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated generic configuration action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "delete": {
            "tags": ["Generic configuration actions"],
            "parameters": [
                {"$ref": "#/components/parameters/generic_configuration_action_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "parameters": {
        "generic_configuration_action_id": {
            "name": "generic_configuration_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    }
}
