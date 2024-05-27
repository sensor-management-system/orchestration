# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Openapi part for the configuration contact roles."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.role import ConfigurationRoleSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(ConfigurationRoleSchema)

paths = {
    "/configuration-contact-roles": {
        "get": {
            "tags": ["Contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of configuration contact roles",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                },
            },
        },
        "post": {
            "tags": ["Contact roles"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created configuration contact role",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
    },
    "/configuration-contact-roles/{configuration_contact_role_id}": {
        "get": {
            "tags": ["Contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/configuration_contact_role_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a configuration contct role",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
        },
        "patch": {
            "tags": ["Contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_contact_role_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Configuration contact role attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the udpated configuration contact role",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
        },
        "delete": {
            "tags": ["Contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_contact_role_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}

components = {
    "parameters": {
        "configuration_contact_role_id": {
            "name": "configuration_contact_role_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
