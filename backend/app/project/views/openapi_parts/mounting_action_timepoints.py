# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for the mounting action timepoints endpoints."""

paths = {
    "/controller/configurations/{configuration_id}/mounting-action-timepoints": {
        "get": {
            "tags": ["Controller"],
            "parameters": [{"$ref": "#/components/parameters/configuration_id"}],
            "responses": {
                "200": {"$ref": "#/components/responses/mountingActionTimepoints_coll"}
            },
        }
    },
}

# Some very long urls.
platformtype2 = "https://localhost.localdomain/cv/api/v1/platformtypes/2/"
equipmenttype51 = "https://localhost.localdomain/cv/api/v1/equipmenttypes/51/"
equipmentstatus1 = "https://localhost.localdomain/cv/api/v1/equipmentstatus/1/"
equipmentstatus2 = "https://localhost.localdomain/cv/api/v1/equipmentstatus/2/"
manufacturer23 = "https://localhost.localdomain/cv/api/v1/manufacturers/23/"
manufacturer25 = "https://localhost.localdomain/cv/api/v1/manufacturers/25/"

components = {
    "responses": {
        "mountingActionTimepoints_coll": {
            "description": "",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": [
                                    {
                                        "timepoint": "2022-07-14T10:51:04",
                                        "type": "platform_mount",
                                        "attributes": {
                                            "description": "",
                                            "inventory_number": "",
                                            "status_name": "In Use",
                                            "model": "",
                                            "short_name": "TIP1",
                                            "website": "",
                                            "created_at": "2022-07-14T08:37:59.375554",
                                            "is_internal": True,
                                            "persistent_identifier": None,
                                            "updated_at": None,
                                            "manufacturer_name": "Agilent Technologies",
                                            "is_private": False,
                                            "platform_type_uri": platformtype2,
                                            "status_uri": equipmentstatus2,
                                            "is_public": False,
                                            "archived": False,
                                            "long_name": "",
                                            "serial_number": "",
                                            "manufacturer_uri": manufacturer23,
                                            "group_ids": ["dpvm-9"],
                                            "platform_type_name": "Drone",
                                        },
                                    },
                                    {
                                        "timepoint": "2022-07-14T11:49:50",
                                        "type": "device_mount",
                                        "attributes": {
                                            "description": "This is just a test device",
                                            "inventory_number": "1236540",
                                            "status_name": "In Warehouse",
                                            "model": "air122",
                                            "short_name": "TID1",
                                            "website": "http://test-device.de",
                                            "created_at": "2022-07-14T08:06:48.510577",
                                            "is_internal": True,
                                            "dual_use": False,
                                            "persistent_identifier": None,
                                            "device_type_name": "Air quality sensor",
                                            "updated_at": None,
                                            "manufacturer_name": "AquaCheck",
                                            "is_private": False,
                                            "status_uri": equipmentstatus1,
                                            "device_type_uri": equipmenttype51,
                                            "is_public": False,
                                            "archived": False,
                                            "long_name": "",
                                            "serial_number": "55se321de",
                                            "manufacturer_uri": manufacturer25,
                                            "group_ids": ["dpvm-9"],
                                        },
                                    },
                                    {
                                        "timepoint": "2022-07-14T11:49:50",
                                        "type": "device_mount",
                                        "attributes": {
                                            "description": "This is just a test device",
                                            "inventory_number": "",
                                            "status_name": "In Warehouse",
                                            "model": "air122",
                                            "short_name": "TID2",
                                            "website": "http://test-device.de",
                                            "created_at": "2022-07-14T11:12:20.679483",
                                            "is_internal": True,
                                            "dual_use": False,
                                            "persistent_identifier": None,
                                            "device_type_name": "Air quality sensor",
                                            "updated_at": None,
                                            "manufacturer_name": "AquaCheck",
                                            "is_private": False,
                                            "status_uri": equipmentstatus1,
                                            "device_type_uri": equipmenttype51,
                                            "is_public": False,
                                            "archived": False,
                                            "long_name": "",
                                            "serial_number": "",
                                            "manufacturer_uri": manufacturer25,
                                            "group_ids": ["dpvm-1"],
                                        },
                                    },
                                ]
                            }
                        }
                    }
                }
            },
        }
    }
}
