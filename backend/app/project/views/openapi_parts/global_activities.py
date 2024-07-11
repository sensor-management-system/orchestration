# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Openapi specification for the activity routes."""

paths = {
    "/controller/global-activities": {
        "get": {
            "tags": ["Controller"],
            "parameters": [
                {
                    "name": "earliest",
                    "in": "query",
                    "required": True,
                    "schema": {"type": "string", "format": "date-time"},
                },
                {
                    "name": "latest",
                    "in": "query",
                    "required": True,
                    "schema": {"type": "string", "format": "date-time"},
                },
            ],
            "responses": {"200": {"$ref": "#/components/responses/GlobalActivity"}},
            "description": "Information about the activity in the SMS.",
            "operationId": "get_global_activity",
        }
    }
}
components = {
    "responses": {
        "GlobalActivity": {
            "description": "Global activity information",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "array",
                                "items": {
                                    "properties": {
                                        "date": {
                                            "type": "string",
                                            "format": "date",
                                        },
                                        "count": {"type": "number"},
                                    }
                                },
                            }
                        },
                    }
                }
            },
        }
    }
}
