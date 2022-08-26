"""Externalized openapi spec for location action timepoints."""

paths = {
    "/controller/configurations/{configuration_id}/location-action-timepoints": {
        "get": {
            "tags": ["Controller"],
            "parameters": [{"$ref": "#/components/parameters/configuration_id"}],
            "responses": {
                "200": {"$ref": "#/components/responses/LocationActionTimepoints_coll"}
            },
        }
    }
}
components = {
    "responses": {
        "LocationActionTimepoints_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "array",
                                "properties": {
                                    "timepoint": {
                                        "type": "string",
                                        "format": "datetime",
                                    },
                                    "type": {"type": "string"},
                                    "id": {"type": "string"},
                                },
                                "example": [
                                    {
                                        "timepoint": "2022-07-14T10:51:04",
                                        "type": "static_location_begin_action",
                                        "id": "123",
                                    },
                                    {
                                        "timepoint": "2022-07-14T11:49:50",
                                        "type": "static_location_end_action",
                                        "id": "123",
                                    },
                                    {
                                        "timepoint": "2022-07-14T11:49:50",
                                        "type": "dynamic_location_begin_action",
                                        "id": "234",
                                    },
                                ],
                            }
                        }
                    }
                }
            },
            "description": "",
        }
    }
}
