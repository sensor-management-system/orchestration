# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

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
                                        "configuration_id": "3",
                                        "configuration_label": "Test configuration",
                                        "begin_date": "2021-01-31T10:00:00Z",
                                        "end_date": "2021-02-28T10:00:00Z",
                                    },
                                    {
                                        "id": "2",
                                        "available": False,
                                        "mount": "124",
                                        "configuration_id": "3",
                                        "configuration_label": "Test configuration",
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
