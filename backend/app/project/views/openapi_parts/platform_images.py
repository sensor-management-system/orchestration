# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.platform_image_schema import PlatformImageSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(PlatformImageSchema)

paths = {
    "/platform-images": {
        "get": {
            "tags": ["Platform images"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of platform images",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve a list of platform images",
            "operationId": "RetrievecollectionofPlatformImageobjects",
        },
        "post": {
            "tags": ["Platform images"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created platform image",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreatePlatformImage",
        },
    },
    "/platform-images/{platform_image_id}": {
        "get": {
            "tags": ["Platform images"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/platform_image_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a platform image",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a single platform image",
            "operationId": "RetrievePlatformImageInstance",
        },
        "patch": {
            "tags": ["Platform images"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_image_id"},
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "PlatformImage attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated platform image",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update PlatformImage attributes",
            "operationId": "UpdatePlatformImage",
        },
        "delete": {
            "tags": ["Platform images"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_image_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeletePlatformImage",
        },
    },
}

components = {
    "parameters": {
        "platform_image_id": {
            "name": "platform_image_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
