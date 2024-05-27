# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""External openapi spec file for the mounting actions endpoints."""

paths = {
    "/controller/configurations/{configuration_id}/mounting-actions": {
        "get": {
            "tags": ["Controller"],
            "description": " ".join(
                [
                    "Returns information of the platforms & devices that are mounted",
                    "on the configuration to the given timepoint.",
                    "Platforms and devices are sorted by short name.",
                ]
            ),
            "parameters": [
                {"$ref": "#/components/parameters/timepoint"},
                {"$ref": "#/components/parameters/configuration_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/mountingActions_coll"}
            },
        }
    }
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
        "mountingActions_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": [
                                    {
                                        "action": {
                                            "data": {
                                                "type": "platform_mount_action",
                                                "relationships": {
                                                    "parent_platform": {
                                                        "data": None,
                                                    },
                                                    "configuration": {
                                                        "data": {
                                                            "type": "configuration",
                                                            "id": "1",
                                                        },
                                                    },
                                                    "platform": {
                                                        "data": {
                                                            "type": "platform",
                                                            "id": "1",
                                                        },
                                                    },
                                                    "begin_contact": {
                                                        "data": {
                                                            "type": "contact",
                                                            "id": "1",
                                                        },
                                                    },
                                                    "created_by": {
                                                        "data": {
                                                            "type": "user",
                                                            "id": "1",
                                                        },
                                                    },
                                                    "updated_by": {
                                                        "data": {
                                                            "type": "user",
                                                            "id": "1",
                                                        },
                                                    },
                                                    "end_contact": {
                                                        "data": None,
                                                    },
                                                },
                                                "attributes": {
                                                    "created_at": "2022-07-14T10:50:53",
                                                    "end_date": None,
                                                    "begin_description": None,
                                                    "begin_date": "2022-07-14T10:51:04",
                                                    "offset_x": None,
                                                    "offset_y": None,
                                                    "end_description": None,
                                                    "updated_at": "2022-07-14T10:50:55",
                                                    "offset_z": None,
                                                },
                                                "id": "1",
                                            },
                                        },
                                        "entity": {
                                            "data": {
                                                "type": "platform",
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
                                                "relationships": {
                                                    "updated_by": {"data": None},
                                                    "platform_attachments": {
                                                        "data": [],
                                                    },
                                                    "contacts": {
                                                        "data": [
                                                            {
                                                                "type": "contact",
                                                                "id": "1",
                                                            }
                                                        ],
                                                    },
                                                    "generic_platform_actions": {
                                                        "data": [
                                                            {
                                                                "type": "generic_platform_action",
                                                                "id": "1",
                                                            },
                                                            {
                                                                "type": "generic_platform_action",
                                                                "id": "2",
                                                            },
                                                        ],
                                                    },
                                                    "platform_mount_actions": {
                                                        "data": [
                                                            {
                                                                "type": "platform_mount_actions",
                                                                "id": "1",
                                                            }
                                                        ],
                                                    },
                                                    "outer_platform_mount_actions": {
                                                        "data": [],
                                                    },
                                                    "outer_device_mount_actions": {
                                                        "data": [
                                                            {
                                                                "type": "device_mount_action",
                                                                "id": "1",
                                                            }
                                                        ],
                                                    },
                                                    "platform_software_update_actions": {
                                                        "data": [],
                                                    },
                                                    "created_by": {
                                                        "data": {
                                                            "type": "user",
                                                            "id": "1",
                                                        },
                                                    },
                                                },
                                                "id": "1",
                                            },
                                        },
                                        "children": [
                                            {
                                                "action": {
                                                    "data": {
                                                        "type": "device_mount_action",
                                                        "relationships": {
                                                            "parent_platform": {
                                                                "data": {
                                                                    "type": "platform",
                                                                    "id": "1",
                                                                },
                                                            },
                                                            "configuration": {
                                                                "data": {
                                                                    "type": "configuration",
                                                                    "id": "1",
                                                                },
                                                            },
                                                            "device": {
                                                                "data": {
                                                                    "type": "device",
                                                                    "id": "1",
                                                                },
                                                            },
                                                            "begin_contact": {
                                                                "data": {
                                                                    "type": "contact",
                                                                    "id": "1",
                                                                },
                                                            },
                                                            "updated_by": {
                                                                "data": {
                                                                    "type": "user",
                                                                    "id": "1",
                                                                },
                                                            },
                                                            "created_by": {
                                                                "data": {
                                                                    "type": "user",
                                                                    "id": "1",
                                                                },
                                                            },
                                                            "end_contact": {
                                                                "data": None
                                                            },
                                                        },
                                                        "attributes": {
                                                            "created_at": "2022-07-14T10:49:36",
                                                            "end_date": None,
                                                            "begin_description": None,
                                                            "begin_date": "2022-07-14T11:49:50",
                                                            "offset_x": None,
                                                            "offset_y": None,
                                                            "end_description": None,
                                                            "updated_at": "2022-07-14T10:49:44",
                                                            "offset_z": None,
                                                        },
                                                        "id": "1",
                                                    },
                                                },
                                                "entity": {
                                                    "data": {
                                                        "type": "device",
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
                                                        "relationships": {
                                                            "device_properties": {
                                                                "data": [
                                                                    {
                                                                        "type": "device_property",
                                                                        "id": "1",
                                                                    },
                                                                    {
                                                                        "type": "device_property",
                                                                        "id": "2",
                                                                    },
                                                                ],
                                                            },
                                                            "updated_by": {
                                                                "data": None
                                                            },
                                                            "contacts": {
                                                                "data": [
                                                                    {
                                                                        "type": "contact",
                                                                        "id": "1",
                                                                    }
                                                                ],
                                                            },
                                                            "device_software_update_actions": {
                                                                "data": [],
                                                            },
                                                            "device_calibration_actions": {
                                                                "data": [],
                                                            },
                                                            "customfields": {
                                                                "data": [
                                                                    {
                                                                        "type": "customfield",
                                                                        "id": "1",
                                                                    }
                                                                ],
                                                            },
                                                            "device_mount_actions": {
                                                                "data": [
                                                                    {
                                                                        "type": "device_mount_action",
                                                                        "id": "1",
                                                                    }
                                                                ],
                                                            },
                                                            "generic_device_actions": {
                                                                "data": [],
                                                            },
                                                            "created_by": {
                                                                "data": {
                                                                    "type": "user",
                                                                    "id": "1",
                                                                },
                                                            },
                                                            "device_attachments": {
                                                                "data": [
                                                                    {
                                                                        "type": "device_attachment",
                                                                        "id": "1",
                                                                    }
                                                                ],
                                                            },
                                                        },
                                                        "id": "1",
                                                    },
                                                },
                                                "children": [],
                                            }
                                        ],
                                    },
                                    {
                                        "action": {
                                            "data": {
                                                "type": "device_mount_action",
                                                "relationships": {
                                                    "parent_platform": {"data": None},
                                                    "configuration": {
                                                        "data": {
                                                            "type": "configuration",
                                                            "id": "1",
                                                        },
                                                    },
                                                    "device": {
                                                        "data": {
                                                            "type": "device",
                                                            "id": "2",
                                                        },
                                                    },
                                                    "begin_contact": {
                                                        "data": {
                                                            "type": "contact",
                                                            "id": "1",
                                                        },
                                                    },
                                                    "updated_by": {
                                                        "data": {
                                                            "type": "user",
                                                            "id": "1",
                                                        },
                                                    },
                                                    "created_by": {
                                                        "data": {
                                                            "type": "user",
                                                            "id": "1",
                                                        },
                                                    },
                                                    "end_contact": {"data": None},
                                                },
                                                "attributes": {
                                                    "created_at": "2022-07-14T10:49:36",
                                                    "end_date": None,
                                                    "begin_description": None,
                                                    "begin_date": "2022-07-14T11:49:50",
                                                    "offset_x": None,
                                                    "offset_y": None,
                                                    "end_description": None,
                                                    "updated_at": "2022-07-14T10:49:44",
                                                    "offset_z": None,
                                                },
                                                "id": "2",
                                            },
                                        },
                                        "entity": {
                                            "data": {
                                                "type": "device",
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
                                                "relationships": {
                                                    "device_properties": {
                                                        "data": [
                                                            {
                                                                "type": "device_property",
                                                                "id": "3",
                                                            },
                                                            {
                                                                "type": "device_property",
                                                                "id": "4",
                                                            },
                                                        ],
                                                    },
                                                    "updated_by": {"data": None},
                                                    "contacts": {
                                                        "data": [],
                                                    },
                                                    "device_software_update_actions": {
                                                        "data": [],
                                                    },
                                                    "device_calibration_actions": {
                                                        "data": [],
                                                    },
                                                    "customfields": {
                                                        "data": [],
                                                    },
                                                    "device_mount_actions": {
                                                        "data": [
                                                            {
                                                                "type": "device_mount_action",
                                                                "id": "2",
                                                            }
                                                        ],
                                                    },
                                                    "generic_device_actions": {
                                                        "data": [],
                                                    },
                                                    "created_by": {
                                                        "data": {
                                                            "type": "user",
                                                            "id": "1",
                                                        },
                                                    },
                                                    "device_attachments": {
                                                        "data": [],
                                                    },
                                                },
                                                "id": "2",
                                            },
                                        },
                                        "children": [],
                                    },
                                ]
                            }
                        }
                    }
                }
            },
            "description": "",
        }
    },
    "parameters": {
        "timepoint": {
            "name": "timepoint",
            "in": "query",
            "required": True,
            "schema": {"type": "string", "format": "datetime"},
        },
    },
}
