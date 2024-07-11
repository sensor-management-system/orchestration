# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.site_image_schema import SiteImageSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(SiteImageSchema)

paths = {
    "/site-images": {
        "get": {
            "tags": ["Site images"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of site images",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve a list of site images",
            "operationId": "RetrievecollectionofSiteImageobjects",
        },
        "post": {
            "tags": ["Site images"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created site image",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreateSiteImage",
        },
    },
    "/site-images/{site_image_id}": {
        "get": {
            "tags": ["Site images"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/site_image_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a site image",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a single site image",
            "operationId": "RetrieveSiteImageInstance",
        },
        "patch": {
            "tags": ["Site images"],
            "parameters": [
                {"$ref": "#/components/parameters/site_image_id"},
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "SiteImage attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated site image",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update SiteImage attributes",
            "operationId": "UpdateSiteImage",
        },
        "delete": {
            "tags": ["Site images"],
            "parameters": [
                {"$ref": "#/components/parameters/site_image_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeleteSiteImage",
        },
    },
}

components = {
    "parameters": {
        "site_image_id": {
            "name": "site_image_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
