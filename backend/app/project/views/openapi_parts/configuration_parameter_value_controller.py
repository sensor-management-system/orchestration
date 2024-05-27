# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Openapi specs for the extraction of configuration parameters by timepoint."""

paths = {
    "/controller/configurations/{configuration_id}/parameter-values": {
        "get": {
            "tags": ["Controller"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_id"},
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
                    "description": "".join(
                        [
                            "List of configuration parameter values to a ",
                            "specific timepoint. Includes platform & device ",
                            "parameters - depending on mount dates.",
                        ]
                    ),
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
                                },
                            }
                        }
                    },
                }
            },
        }
    }
}
