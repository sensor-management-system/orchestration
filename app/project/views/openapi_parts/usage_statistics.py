"""
Openapi parts for the usage statistics endpoints.

Important for this module are the dicts for paths
and components.
"""

paths = {
    "/usage-statistics": {
        "get": {
            "tags": ["Usage statistics"],
            "parameters": [],
            "responses": {"200": {"$ref": "#/components/responses/UsageStatistics"}},
            "description": "User info about the current usage of the sms instance.",
            "operationId": "get_usage_statistics",
        }
    }
}
components = {
    "responses": {
        "UsageStatistics": {
            "description": "Usage statistic informations",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "counts": {
                                "type": "object",
                                "properties": {
                                    "devices": {"type": "number"},
                                    "platforms": {"type": "number"},
                                    "configurations": {"type": "number"},
                                    "users": {"type": "number"},
                                },
                                "example": {
                                    "devices": 300,
                                    "platforms": 100,
                                    "configurations": 70,
                                    "users": 50,
                                },
                            }
                        }
                    }
                }
            },
        }
    }
}
