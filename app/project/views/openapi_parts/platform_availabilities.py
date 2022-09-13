"""External openapi spec file for platform availabilities."""
paths = {
    "/controller/platform-availabilities": {
        "get": {
            "tags": ["Controller"],
            "parameters": [
                {"$ref": "#/components/parameters/ids"},
                {"$ref": "#/components/parameters/from"},
                {"$ref": "#/components/parameters/to"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/PlatformAvailabilities_coll"}
            },
        }
    }
}
components = {
    "responses": {
        "PlatformAvailabilities_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": [
                                    {
                                        "id": "1",
                                        "available": False,
                                        "mount": "123",
                                        "configuration": "3",
                                        "begin_date": "2021-01-31T10:00:00Z",
                                        "end_date": "2021-02-28T10:00:00Z",
                                    },
                                    {
                                        "id": "2",
                                        "available": False,
                                        "mount": "124",
                                        "configuration": "3",
                                        "begin_date": "2021-01-31T10:00:00Z",
                                        "end_date": "2021-02-28T10:00:00Z",
                                    },
                                    {"id": "3", "available": True},
                                ]
                            }
                        }
                    }
                }
            },
            "description": "",
        }
    }
}
