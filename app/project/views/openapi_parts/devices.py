"""External openapi spec file for the device endpoints."""
paths = {
    "/devices/{device_id}/archive": {
        "post": {
            "tags": ["Device"],
            "parameters": [
                {"$ref": "#/components/parameters/device_id"},
            ],
            "responses": {
                "204": {"description": "Device was archived succesfully."},
                "401": {"$ref": "#/components/errors/authentification_required"},
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
                "409": {"$ref": "#/components/errors/conflict"},
            },
            "description": "Archive a device.",
            "operationId": "ArchiveDevice",
        }
    },
    "/devices/{device_id}/restore": {
        "post": {
            "tags": ["Device"],
            "parameters": [
                {"$ref": "#/components/parameters/device_id"},
            ],
            "responses": {
                "204": {"description": "Restoring of the device was succesful."},
                "401": {"$ref": "#/components/errors/authentification_required"},
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Restore an archived device.",
            "operationId": "RestoreDevice",
        }
    },
}
components = {}
