"""
Openapi parts for the user info endpoints.

Important for this module are the dicts for paths
and components.
"""

paths = {
    "/user-info": {
        "get": {
            "tags": ["User info"],
            "parameters": [],
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
                                            "admin": {"type": "array"},
                                            "member": {"type": "array"},
                                            "active": {"type": "boolean"},
                                            "is_superuser": {"type": "boolean"},
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
