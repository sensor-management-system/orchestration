# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for platform attachments."""

paths = {
    "/platform-attachments": {
        "get": {
            "tags": ["Platform attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {
                    "name": "filter[label]",
                    "in": "query",
                    "required": False,
                    "description": "label attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {"$ref": "#/components/parameters/url"},
                {"$ref": "#/components/parameters/id"},
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/PlatformAttachment_coll"}
            },
            "description": "Retrieve PlatformAttachment from platform_attachment",
            "operationId": "RetrieveacollectionofPlatformAttachmentobjects_0",
        },
        "post": {
            "tags": ["Platform attachments"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {
                            "$ref": "#/components/schemas/PlatformAttachmentPost"
                        }
                    }
                },
                "description": "PlatformAttachment attributes",
                "required": True,
            },
            "responses": {
                "201": {"$ref": "#/components/responses/PlatformAttachment_single"},
                "401": {"$ref": "#/components/errors/authentification_required"},
            },
            "operationId": "CreatePlatformAttachment_0",
        },
    },
    "/platform-attachments/{platform_attachment_id}": {
        "get": {
            "tags": ["Platform attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/platform_attachment_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/PlatformAttachment_single"}
            },
            "description": "Retrieve PlatformAttachment from platform_attachment",
            "operationId": "RetrievePlatformAttachmentinstance_0",
        },
        "patch": {
            "tags": ["Platform attachments"],
            "parameters": [{"$ref": "#/components/parameters/platform_attachment_id"}],
            "requestBody": {
                "$ref": "#/components/requestBodies/PlatformAttachment_inst"
            },
            "responses": {
                "200": {"$ref": "#/components/responses/PlatformAttachment_single"},
                "401": {"$ref": "#/components/errors/authentification_required"},
                "404": {"$ref": "#/components/errors/not_found"},
                "409": {"$ref": "#/components/errors/conflict"},
            },
            "description": "Update PlatformAttachment attributes",
            "operationId": "UpdatePlatformAttachment_0",
        },
        "delete": {
            "tags": ["Platform attachments"],
            "parameters": [{"$ref": "#/components/parameters/platform_attachment_id"}],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "401": {"$ref": "#/components/errors/authentification_required"},
                "404": {"$ref": "#/components/errors/not_found"},
            },
            "operationId": "DeletePlatformAttachmentfromplatformattachment_0",
        },
    },
    "/platform-attachments/{platform_attachment_id}/file/{filename}": {
        "get": {
            "tags": ["Platform attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_attachment_id"},
                {
                    "name": "filename",
                    "in": "path",
                    "required": True,
                    "description": (
                        "Filename of the file. Can be arbitrary, it "
                        "will always return the same file - no matter "
                        "how this parameter is set. "
                        "Backend needs this to allow linking of filenames for uploads."
                    ),
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
                    "$ref": "#/components/errors/authentification_required",
                },
                "404": {
                    "$ref": "#/components/errors/not_found",
                },
            },
            "description": "Endpoint to get the content of the uploaded file.",
        }
    },
}

components = {
    "requestBodies": {
        "PlatformAttachment_inst": {
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
                                        },
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "required": ["platform"],
                                        "properties": {
                                            "platform": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "platform_attachment",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            }
                                        },
                                    },
                                    "type": {"type": "string"},
                                },
                            }
                        },
                        "description": "PlatformAttachment patch;",
                    }
                }
            }
        },
    },
    "schemas": {
        "PlatformAttachmentPost": {
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "attributes": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "url": {"type": "string", "format": "url"},
                            },
                        },
                        "type": {"type": "string"},
                        "id": {"type": "string"},
                    },
                    "example": {
                        "attributes": {"label": "", "url": ""},
                        "relationships": {
                            "platform": {"data": {"type": "platform", "id": "0"}}
                        },
                        "type": "platform_attachment",
                    },
                }
            },
            "description": "PlatformAttachment post;",
        },
    },
    "responses": {
        "PlatformAttachment_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "list",
                                "properties": {
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "label": {"type": "string"},
                                            "url": {"type": "string", "format": "url"},
                                            "is_internal": {"type": "boolean"},
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
                                            "platform": {
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
                                "example": [
                                    {
                                        "attributes": {
                                            "label": "",
                                            "url": "",
                                            "is_upload": False,
                                            "created_at": "2023-03-14T12:00:00+00:00",
                                            "updated_at": "2023-03-14T13:00:00+00:00",
                                        },
                                        "relationships": {
                                            "platform": {
                                                "data": {"type": "platform", "id": "0"}
                                            },
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
                                        "type": "platform_attachment",
                                        "id": "0",
                                    }
                                ],
                            }
                        },
                        "description": "PlatformAttachment get;",
                    }
                }
            },
            "description": "Platform Attachment",
        },
        "PlatformAttachment_single": {
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
                                            "is_upload": {"type": "boolean"},
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
                                            "platform": {
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
                                        "platform": {
                                            "data": {"type": "platform", "id": "0"}
                                        },
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
                                    "type": "platform_attachment",
                                    "id": "0",
                                },
                            }
                        },
                        "description": "PlatformAttachment get;",
                    }
                }
            },
            "description": "Platform Attachment",
        },
    },
    "parameters": {
        "platform_attachment_id": {
            "name": "platform_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
