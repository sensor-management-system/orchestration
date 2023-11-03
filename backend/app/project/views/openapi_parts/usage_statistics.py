# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""
Openapi parts for the usage statistics endpoints.

Important for this module are the dicts for paths
and components.
"""

paths = {
    "/usage-statistics": {
        "get": {
            "tags": ["Usage statistics"],
            "parameters": [
                {
                    "name": "extended",
                    "description": "Show some more information (pids, uploads, organizations, ...)",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "boolean", "default": "false"},
                }
            ],
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
