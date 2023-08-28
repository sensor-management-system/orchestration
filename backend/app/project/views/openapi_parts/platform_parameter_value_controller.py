# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Openapi specs for the extraction of platform parameters by timepoint."""

paths = {
    "/controller/platforms/{platform_id}/parameter-values": {
        "get": {
            "tags": ["Controller"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_id"},
                {
                    "name": "timepoint",
                    "in": "query",
                    "required": True,
                    "schema": {
                        "type": "string",
                        "format": "date-time",
                    },
                },
            ],
            "responses": {
                "200": {
                    "description": "List of platform parameter values to a specific timepoint.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "properties": {
                                    "data": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "type": {"type": "string"},
                                                "attributes": {
                                                    "type": "object",
                                                    "properties": {
                                                        "label": {
                                                            "type": "string",
                                                        },
                                                        "value": {
                                                            "type": "string",
                                                        },
                                                        "unit_name": {
                                                            "type": "string",
                                                        },
                                                        "unit_uri": {"type": "string"},
                                                    },
                                                },
                                            },
                                        },
                                    }
                                }
                            }
                        }
                    },
                }
            },
        }
    }
}
