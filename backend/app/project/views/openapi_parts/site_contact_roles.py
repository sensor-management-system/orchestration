# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Openapi part for the site contact roles."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.role import SiteRoleSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(SiteRoleSchema)

paths = {
    "/site-contact-roles": {
        "get": {
            "tags": ["Site contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of site contact roles",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                },
            },
        },
        "post": {
            "tags": ["Site contact roles"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created site contact role",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
    },
    "/site-contact-roles/{site_contact_role_id}": {
        "get": {
            "tags": ["Site contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/site_contact_role_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a site contct role",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
        },
        "patch": {
            "tags": ["Site contact roles"],
            "parameters": [{"$ref": "#/components/parameters/site_contact_role_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Site contact role attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the udpated site contact role",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
        },
        "delete": {
            "tags": ["Site contact roles"],
            "parameters": [{"$ref": "#/components/parameters/site_contact_role_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}

components = {
    "parameters": {
        "site_contact_role_id": {
            "name": "site_contact_role_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
