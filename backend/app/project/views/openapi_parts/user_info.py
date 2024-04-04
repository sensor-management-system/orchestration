# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""
Openapi parts for the user info endpoints.

Important for this module are the dicts for paths
and components.
"""

paths = {
    "/user-info": {
        "get": {
            "tags": ["User info"],
            "parameters": [
                {
                    "name": "skip_cache",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "boolean", "default": False},
                }
            ],
            "responses": {"200": {"$ref": "#/components/responses/Userinfo"}},
            "description": "User info for the current user.",
            "operationId": "get_user_info",
        }
    }
}
components = {
    "responses": {
        "Userinfo": {
            "description": "User informations",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {"type": "string", "default": "user"},
                                    "id": {"type": "string"},
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "admin": {
                                                "type": "array",
                                                "items": {"type": "string"},
                                            },
                                            "member": {
                                                "type": "array",
                                                "items": {"type": "string"},
                                            },
                                            "active": {"type": "boolean"},
                                            "is_superuser": {"type": "boolean"},
                                            "is_export_control": {"type": "boolean"},
                                            "apikey": {"type": "string"},
                                            "subject": {"type": "string"},
                                        },
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "properties": {
                                            "contact": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "contact",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            }
                                        },
                                    },
                                },
                                "example": {
                                    "type": "user",
                                    "id": "1234",
                                    "attributes": {
                                        "admin": ["12345", "6789"],
                                        "member": ["12345", "998"],
                                        "active": True,
                                        "is_superuser": False,
                                        "is_export_control": False,
                                        "apikey": "123456...",
                                        "subject": "user1234@localhost",
                                    },
                                    "relationships": {
                                        "contact": {
                                            "data": {
                                                "type": "contact",
                                                "id": "123",
                                            }
                                        }
                                    },
                                },
                            }
                        }
                    }
                }
            },
        }
    }
}
