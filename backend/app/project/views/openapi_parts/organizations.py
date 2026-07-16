# SPDX-FileCopyrightText: 2026
# - Nils Brinckmann <nils.brinckmann@gfz.de>
# - GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Openapi spec file for the organizations."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.organization_schema import OrganizationSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(OrganizationSchema)

paths = {
    "/organizations": {
        "get": {
            "tags": ["Organizations"],
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
                    "description": "List of organizations",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve the list of organizations",
            "operationId": "RetrieveacollectionofOrganizationobjects_0",
        },
        "post": {
            "tags": ["Organizations"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created Organization",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "operationId": "CreateOrganization_0",
            "parameters": [],
        },
    },
    "/organizations/{organization_id}": {
        "get": {
            "tags": ["Organizations"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/organization_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of an organization",
                    "content": {
                        "application/vnd.api.json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Retrieve a single organization",
            "operationId": "RetrieveOrganizationinstance_0",
        },
        "patch": {
            "tags": ["Organizations"],
            "parameters": [{"$ref": "#/components/parameters/organization_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Device attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated organization",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Update organization attributes",
            "operationId": "UpdateOrganization_0",
        },
        "delete": {
            "tags": ["Organizations"],
            "parameters": [{"$ref": "#/components/parameters/organization_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteOrganizationfromdevice_3",
        },
    },
}
components = {
    "parameters": {
        "organization_id": {
            "name": "organization_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string", "default": "0"},
        }
    }
}
