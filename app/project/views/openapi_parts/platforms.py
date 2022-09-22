"""External openapi spec file for the platform endpoints."""
paths = {
    "/platforms/{platform_id}/archive": {
        "post": {
            "tags": ["Platform"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_id"},
            ],
            "responses": {
                "204": {"description": "Platform was archived succesfully."},
                "401": {"$ref": "#/components/errors/authentification_required"},
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
                "409": {"$ref": "#/components/errors/conflict"},
            },
            "description": "Archive a platform.",
            "operationId": "ArchivePlatform",
        }
    },
    "/platforms/{platform_id}/restore": {
        "post": {
            "tags": ["Platform"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_id"},
            ],
            "responses": {
                "204": {"description": "Restoring of the platform was succesful."},
                "401": {"$ref": "#/components/errors/authentification_required"},
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Restore an archived platform.",
            "operationId": "RestorePlatform",
        }
    },
}
components = {}
