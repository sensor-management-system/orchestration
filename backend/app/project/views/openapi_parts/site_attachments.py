# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for site attachments."""
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
                "200": {"$ref": "#/components/responses/SiteAttachment_coll"}
            },
            "description": "Retrieve SiteAttachment from site_attachment",
            "operationId": "RetrieveacollectionofSiteAttachmentobjects_0",
        },
        "post": {
            "tags": ["Site attachments"],
            "requestBody": {"$ref": "#/components/requestBodies/SiteAttachment_inst"},
            "responses": {
                "201": {"$ref": "#/components/responses/SiteAttachment_coll"}
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
                "200": {"$ref": "#/components/responses/SiteAttachment_coll"}
            },
            "description": "Retrieve SiteAttachment from site_attachment",
            "operationId": "RetrieveSiteAttachmentinstance_0",
        },
        "patch": {
            "tags": ["Site attachments"],
            "parameters": [{"$ref": "#/components/parameters/site_attachment_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/SiteAttachment"}
                    }
                },
                "description": "SiteAttachment attributes",
                "required": True,
            },
            "responses": {
                "200": {"$ref": "#/components/responses/SiteAttachment_coll"}
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
    "requestBodies": {
        "SiteAttachment_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "site_attachment",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "required": ["label", "url"],
                                        "properties": {
                                            "label": {"type": "string"},
                                            "url": {"type": "string", "format": "url"},
                                        },
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "required": ["site"],
                                        "properties": {
                                            "site": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": ("site"),
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            }
                                        },
                                    },
                                },
                            }
                        },
                        "description": "SiteAttachment post;",
                    }
                }
            }
        },
    },
    "schemas": {
        "SiteAttachment": {
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "attributes": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "url": {"type": "string", "format": "url"},
                                "is_upload": {"type": "boolean"},
                            },
                        },
                        "type": {"type": "string"},
                        "id": {"type": "string"},
                    },
                    "example": {
                        "attributes": {"label": "", "url": ""},
                        "type": "site_attachment",
                        "id": "0",
                    },
                }
            },
            "description": "SiteAttachment Schema;",
        },
    },
    "responses": {
        "SiteAttachment_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "label": {"type": "string"},
                                            "url": {"type": "string", "format": "url"},
                                            "is_upload": {
                                                "type": "boolean",
                                            },
                                            "created_at": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                            "updated_at": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                        },
                                    },
                                    "type": {"type": "string"},
                                    "id": {"type": "string"},
                                    "relationships": {
                                        "type": "object",
                                        "properties": {
                                            "site": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                            "created_by": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                            "updated_by": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                        },
                                    },
                                },
                                "example": {
                                    "attributes": {
                                        "label": "",
                                        "url": "",
                                        "is_upload": False,
                                        "created_at": "2023-03-14T12:00:00+00:00",
                                        "updated_at": "2023-03-14T13:00:00+00:00",
                                    },
                                    "relationships": {
                                        "site": {"data": {"type": "site", "id": "0"}},
                                        "created_by": {
                                            "data": {
                                                "type": "user",
                                                "id": "123",
                                            }
                                        },
                                        "updated_by": {
                                            "data": {
                                                "type": "user",
                                                "id": "124",
                                            }
                                        },
                                    },
                                    "type": "site_attachment",
                                    "id": "0",
                                },
                            }
                        },
                        "description": "SiteAttachment get;",
                    }
                }
            },
            "description": "SiteAttachment",
        },
    },
    "parameters": {
        "site_attachment_id": {
            "name": "site_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
