# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Openapi specification for the part about the export control attachments."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.export_control_attachment_schema import (
    ExportControlAttachmentSchema,
)

schema_mapper = MarshmallowJsonApiToOpenApiMapper(ExportControlAttachmentSchema)

paths = {
    "/export-control-attachments": {
        "get": {
            "tags": ["Export control attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of export control attachments",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve a list of export control attachments",
            "operationId": "RetrievecollectionofExportControlAttachmentobjects",
        },
        "post": {
            "tags": ["Export control attachments"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created export control attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreateExportControlAttachment",
        },
    },
    "/export-control-attachments/{export_control_attachment_id}": {
        "get": {
            "tags": ["Export control attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/export_control_attachment_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of export control attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a single export control attachment",
            "operationId": "RetrieveExportControlAttachmentInstance",
        },
        "patch": {
            "tags": ["Export control attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/export_control_attachment_id"},
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Export control attachment attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated export control attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update ExportControlAttachment attributes",
            "operationId": "UpdateExportControlAttachment",
        },
        "delete": {
            "tags": ["Export control attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/export_control_attachment_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeleteExportControlAttachment",
        },
    },
    "/export-control-attachments/{export_control_attachment_id}/file/{filename}": {
        "get": {
            "tags": ["Export control attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/export_control_attachment_id"},
                {
                    "name": "filename",
                    "in": "path",
                    "required": True,
                    "description": (
                        "Filename of the file. Can be arbitrary, it "
                        "will always return the same file - no matter"
                        " how this parameter is set. "
                        "Backend needs this to allow linking of filenames for uploads."
                    ),
                    "schema": {"type": "string", "default": "file"},
                },
            ],
            "responses": {
                "200": {
                    "description": (
                        "Content of the file. Content-Type is the "
                        "same as the original upload."
                    ),
                },
                "401": {
                    "description": "Authentification required.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/authentification_required"
                            }
                        }
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Endpoint to get the content of the uploaded file.",
        }
    },
}

components = {
    "parameters": {
        "export_control_attachment_id": {
            "name": "export_control_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
