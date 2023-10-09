# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for site attachments."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.site_attachment_schema import SiteAttachmentSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(SiteAttachmentSchema)

paths = {
    "/site-attachments": {
        "get": {
            "tags": ["Site attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {"$ref": "#/components/parameters/label"},
                {"$ref": "#/components/parameters/url"},
                {"$ref": "#/components/parameters/id"},
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {
                "200": {
                    "description": "List of site attachments",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve SiteAttachment from site_attachment",
            "operationId": "RetrieveacollectionofSiteAttachmentobjects_0",
        },
        "post": {
            "tags": ["Site attachments"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created site attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreateSiteAttachment_0",
        },
    },
    "/site-attachments/{site_attachment_id}": {
        "get": {
            "tags": ["Site attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/site_attachment_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a site attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Retrieve SiteAttachment from site_attachment",
            "operationId": "RetrieveSiteAttachmentinstance_0",
        },
        "patch": {
            "tags": ["Site attachments"],
            "parameters": [{"$ref": "#/components/parameters/site_attachment_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "SiteAttachment attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated site attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "description": "Update SiteAttachment attributes",
            "operationId": "UpdateSiteAttachment_0",
        },
        "delete": {
            "tags": ["Site attachments"],
            "parameters": [{"$ref": "#/components/parameters/site_attachment_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteSiteAttachmentfromsiteattachment_0",
        },
    },
    "/site-attachments/{site_attachment_id}/file/{filename}": {
        "get": {
            "tags": ["Site attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/site_attachment_id"},
                {
                    "name": "filename",
                    "in": "path",
                    "required": True,
                    "description": (
                        "Filename of the file. Can be arbitrary, "
                        "it will always return the same file - no "
                        "matter how this parameter is set. "
                        "Backend needs this to allow linking of filenames for uploads."
                    ),
                    "schema": {"type": "string", "default": "file"},
                },
            ],
            "responses": {
                "200": {
                    "description": (
                        "Content of the file. Content-Type "
                        "is the same as the original upload."
                    )
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
            "description": ("Endpoint to get the content of the uploaded file."),
        }
    },
}
components = {
    "parameters": {
        "site_attachment_id": {
            "name": "site_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
