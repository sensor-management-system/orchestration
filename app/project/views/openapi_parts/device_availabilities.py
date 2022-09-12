"""External openapi spec file for the device availabilities."""
paths = {
    "/controller/device-availabilities": {
        "get": {
            "tags": ["Controller"],
            "parameters": [
                {"$ref": "#/components/parameters/ids"},
                {"$ref": "#/components/parameters/from"},
                {"$ref": "#/components/parameters/to"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/DeviceAvailabilities_coll"}
            },
        }
    }
}
components = {
    "responses": {
        "DeviceAvailabilities_coll": {
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
                                        "mount": "134",
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
