# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

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
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "array",
                                "items": {
                                    "properties": {
                                        "timepoint": {
                                            "type": "string",
                                            "format": "datetime",
                                        },
                                        "type": {"type": "string"},
                                        "id": {"type": "string"},
                                        "label": {"type": "string"},
                                    },
                                },
                                "example": [
                                    {
                                        "timepoint": "2022-07-14T10:51:04",
                                        "type": "static_location_begin_action",
                                        "id": "123",
                                        "label": "Somewhere",
                                    },
                                    {
                                        "timepoint": "2022-07-14T11:49:50",
                                        "type": "static_location_end_action",
                                        "id": "123",
                                        "label": "Somewhere",
                                    },
                                    {
                                        "timepoint": "2022-07-14T11:49:50",
                                        "type": "dynamic_location_begin_action",
                                        "id": "234",
                                        "label": "flexible",
                                    },
                                ],
                            }
                        },
                    }
                }
            },
            "description": "",
        }
    }
}
