# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Openapi specification for the part about the export control."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.export_control_schema import ExportControlSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(ExportControlSchema)

paths = {
    "/export-control": {
        "get": {
            "tags": ["Export control"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of export control information",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve a list of export control information",
            "operationId": "RetrievecollectionofExportControlobjects",
        },
        "post": {
            "tags": ["Export control"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created export control information",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreateExportControl",
        },
    },
    "/export-control/{export_control_id}": {
        "get": {
            "tags": ["Export control"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/export_control_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of export control information",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a single export control information",
            "operationId": "RetrieveExportControlInstance",
        },
        "patch": {
            "tags": ["Export control"],
            "parameters": [
                {"$ref": "#/components/parameters/export_control_id"},
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Export control attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated export control information",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update ExportControl attributes",
            "operationId": "UpdateExportControl",
        },
        "delete": {
            "tags": ["Export control"],
            "parameters": [
                {"$ref": "#/components/parameters/export_control_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeleteExportControl",
        },
    },
}

components = {
    "parameters": {
        "export_control_id": {
            "name": "export_control_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
