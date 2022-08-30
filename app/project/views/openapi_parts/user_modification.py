"""Paths & components to describe the endpoints to modify user data."""

paths = {
    "/revoke-apikey": {
        "post": {
            "description": "Revoke the current apikey for the current user and generate a new one.",
            "tags": ["User modification"],
            "parameters": [],
            "responses": {
                "200": {"$ref": "#/components/responses/RevokeApikey"},
                "401": {"$ref": "#/components/errors/authentification_required"},
            },
            "requestBody": {"$ref": "#/components/requestBodies/RevokeApikey"},
        }
    }
}
components = {
    "requestBodies": {
        "RevokeApikey": {
            "description": "Payload to revoke apikeys",
            "content": {"application/vnd.api+json": {"schema": {"properties": {}}}},
        }
    },
    "responses": {
        "RevokeApikey": {
            "description": "Updated apikey",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "user",
                                    },
                                    "id": {
                                        "type": "string",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "properties": {"apikey": {"type": "string"}},
                                    },
                                },
                                "example": {
                                    "type": "user",
                                    "id": "1234",
                                    "attributes": {"apikey": "234567..."},
                                },
                            }
                        }
                    }
                }
            },
        }
    },
}
