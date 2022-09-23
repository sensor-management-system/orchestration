"""External openapi spec file for the configuration endpoints."""
paths = {
    "/configurations/{configuration_id}/archive": {
        "post": {
            "tags": ["Configuration"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_id"},
            ],
            "responses": {
                "204": {"description": "Configuration was archived succesfully."},
                "401": {"$ref": "#/components/errors/authentification_required"},
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
                "409": {"$ref": "#/components/errors/conflict"},
            },
            "description": "Archive a configuration.",
            "operationId": "ArchiveConfiguration",
        }
    },
    "/configurations/{configuration_id}/restore": {
        "post": {
            "tags": ["Configuration"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_id"},
            ],
            "responses": {
                "204": {"description": "Restoring of the configuration was succesful."},
                "401": {"$ref": "#/components/errors/authentification_required"},
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Restore an archived configuration.",
            "operationId": "RestoreConfiguration",
        }
    },
}
components = {}
