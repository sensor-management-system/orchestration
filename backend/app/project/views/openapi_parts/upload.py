# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for the upload endpoint."""

paths = {
    "/upload": {
        "post": {
            "tags": ["Upload"],
            "requestBody": {
                "content": {
                    "multipart/form-data": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "file": {
                                    "description": "The file to upload.",
                                    "type": "string",
                                    "format": "binary",
                                }
                            },
                            "required": ["file"],
                        }
                    }
                }
            },
            "responses": {"201": {"$ref": "#/components/responses/Upload_inst1"}},
            "operationId": "UploadAttachment_0",
            "parameters": [],
        }
    },
}

components = {
    "responses": {
        "Upload_inst1": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "example": {
                                    "message": "object stored in sms-attachments",
                                    "url": "",
                                }
                            }
                        },
                    }
                }
            },
            "description": "Upload successful.",
        },
    }
}
