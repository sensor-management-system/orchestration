# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Part of the openapi for datastream links."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.datastream_link_schema import DatastreamLinkSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(DatastreamLinkSchema)

paths = {
    "/datastream-links": {
        "get": {
            "tags": ["Datastream links"],
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
                    "description": "List of datastream links",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    }
                }
            },
            "description": "Retrieve a collection of datastream link objects",
            "operationId": "RetrieveacollectionofDatastreamLinkObjects",
        },
        "post": {
            "tags": ["Datastream links"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created datastream link",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    }
                }
            },
            "operationId": "CreateDatastreamLink",
        },
    },
    "/datastream-links/{datastream_link_id}": {
        "get": {
            "tags": ["Datastream links"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/datastream_link_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a datastream link",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Retrieve a single datastream link object",
            "operationId": "RetrieveinstanceofDatastreamLinkObject",
        },
        "patch": {
            "tags": ["Datastream links"],
            "parameters": [
                {"$ref": "#/components/parameters/datastream_link_id"},
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Datastream link attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated datastream link",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Update a datastream link object",
            "operationId": "UpdateDatastreamLinkObject",
        },
        "delete": {
            "tags": ["Datastream links"],
            "parameters": [
                {"$ref": "#/components/parameters/datastream_link_id"},
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "Delete a datastream link object",
        },
    },
}
components = {
    "parameters": {
        "datastream_link_id": {
            "name": "datastream_link_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
