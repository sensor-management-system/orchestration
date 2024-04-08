# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Luca Johannes Nendel <Luca-Johannes.Nendel@ufz.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Openapi docs helper file for the free text endpoints."""


def template(endpoint, description, operation_id, response_description):
    """Return the contents for the single endpoint."""
    return {
        endpoint: {
            "get": {
                "tags": [
                    "Controller",
                ],
                "responses": {
                    "200": {
                        "content": {
                            "application/vnd.api+json": {
                                "schema": {
                                    "properties": {
                                        "data": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                        }
                                    }
                                }
                            }
                        },
                        "description": response_description,
                    },
                    "401": {
                        "description": "Authentification required.",
                        "content": {
                            "application/vnd.api+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/authentification_required"
                                }
                            }
                        },
                    },
                },
                "description": description,
                "operationId": operation_id,
            }
        }
    }


paths = {
    "/controller/platform-serial-numbers": {
        "get": {
            "tags": [
                "Controller",
            ],
            "parameters": [
                {
                    "in": "query",
                    "name": "ignore",
                    "schema": {
                        "type": "string",
                    },
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to ignore certain platform ids (given",
                            " as comma seperated numbers) when extracting ",
                            "the set of serial numbers.",
                        ]
                    ),
                },
                {
                    "in": "query",
                    "name": "short_name",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given short name.",
                        ]
                    ),
                },
                {
                    "in": "query",
                    "name": "manufacturer_name",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given manufacturer name.",
                        ]
                    ),
                },
                {
                    "in": "query",
                    "name": "manufacturer_uri",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given manufacturer uri.",
                        ]
                    ),
                },
                {
                    "in": "query",
                    "name": "model",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given model.",
                        ]
                    ),
                },
            ],
            "responses": {
                "200": {
                    "description": "Distinct list of serial numbers.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "properties": {
                                    "data": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    }
                                }
                            }
                        }
                    },
                },
                "401": {
                    "description": "Authentification required.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/authentification_required"
                            }
                        }
                    },
                },
            },
            "description": "Get the list of distinct serial numbers of all platforms.",
            "operationId": "controller_platform_serial_numbers",
        }
    },
    "/controller/device-serial-numbers": {
        "get": {
            "tags": [
                "Controller",
            ],
            "parameters": [
                {
                    "in": "query",
                    "name": "ignore",
                    "schema": {
                        "type": "string",
                    },
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to ignore certain device ids (given",
                            " as comma seperated numbers) when extracting ",
                            "the set of serial numbers.",
                        ]
                    ),
                },
                {
                    "in": "query",
                    "name": "short_name",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given short name.",
                        ]
                    ),
                },
                {
                    "in": "query",
                    "name": "manufacturer_name",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given manufacturer name.",
                        ]
                    ),
                },
                {
                    "in": "query",
                    "name": "manufacturer_uri",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given manufacturer uri.",
                        ]
                    ),
                },
                {
                    "in": "query",
                    "name": "model",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given model.",
                        ]
                    ),
                },
            ],
            "responses": {
                "200": {
                    "description": "List of distinct serial numbers for devices.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "properties": {
                                    "data": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    }
                                }
                            }
                        }
                    },
                },
                "401": {
                    "description": "Authentification required.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/authentification_required"
                            }
                        }
                    },
                },
            },
            "description": "Get the list of distinct serial numbers of all devices.",
            "operationId": "controller_device_serial_numbers",
        }
    },
    "/controller/platform-models": {
        "get": {
            "tags": [
                "Controller",
            ],
            "parameters": [
                {
                    "in": "query",
                    "name": "manufacturer_name",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given manufacturer name.",
                        ]
                    ),
                },
                {
                    "in": "query",
                    "name": "manufacturer_uri",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given manufacturer uri.",
                        ]
                    ),
                },
            ],
            "responses": {
                "200": {
                    "description": "List of distinct models for platforms.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "properties": {
                                    "data": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    }
                                }
                            }
                        }
                    },
                },
                "401": {
                    "description": "Authentification required.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/authentification_required"
                            }
                        }
                    },
                },
            },
            "description": "Get the list of distinct models of all platforms.",
            "operationId": "controller_platform_models",
        }
    },
    "/controller/device-models": {
        "get": {
            "tags": [
                "Controller",
            ],
            "parameters": [
                {
                    "in": "query",
                    "name": "manufacturer_name",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given manufacturer name.",
                        ]
                    ),
                },
                {
                    "in": "query",
                    "name": "manufacturer_uri",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given manufacturer uri.",
                        ]
                    ),
                },
            ],
            "responses": {
                "200": {
                    "description": "List of distinct models for devices.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "properties": {
                                    "data": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    }
                                }
                            }
                        }
                    },
                },
                "401": {
                    "description": "Authentification required.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/authentification_required"
                            }
                        }
                    },
                },
            },
            "description": "Get the list of distinct models of all devices.",
            "operationId": "controller_device_models",
        }
    },
    "/controller/configuration-campaigns": {
        "get": {
            "tags": [
                "Controller",
            ],
            "parameters": [
                {
                    "in": "query",
                    "name": "project",
                    "schema": {"type": "string"},
                    "required": False,
                    "description": "".join(
                        [
                            "Parameter to filter for a given project.",
                        ]
                    ),
                },
            ],
            "responses": {
                "200": {
                    "description": "List of distinct campaigns for configurations.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "properties": {
                                    "data": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    }
                                }
                            }
                        }
                    },
                },
            },
            "description": "Get the list of distinct campaigns of all configurations.",
            "operationId": "controller_configuration_campaigns",
        }
    },
    **template(
        endpoint="/controller/device-short-names",
        description="Get the list of distinct short names of all devices.",
        operation_id="controller_device_short_names",
        response_description="List of distinct short names for devices.",
    ),
    **template(
        endpoint="/controller/device-long-names",
        description="Get the list of distinct long names of all devices.",
        operation_id="controller_device_long_names",
        response_description="List of distinct long names for devices.",
    ),
    **template(
        endpoint="/controller/platform-short-names",
        description="Get the list of distinct short names of all platforms.",
        operation_id="controller_platform_short_names",
        response_description="List of distinct short names for platforms.",
    ),
    **template(
        endpoint="/controller/platform-long-names",
        description="Get the list of distinct long names of all platforms.",
        operation_id="controller_platform_long_names",
        response_description="List of distinct long names for platforms.",
    ),
    **template(
        endpoint="/controller/device-manufacturer-names",
        description="Get the list of distinct manufacturer names of all devices.",
        operation_id="controller_device_manufacturer_names",
        response_description="List of distinct manufacturer names for devices.",
    ),
    **template(
        endpoint="/controller/platform-manufacturer-names",
        description="Get the list of distinct manufacturer names of all platforms.",
        operation_id="controller_platform_manufacturer_names",
        response_description="List of distinct manufacturer names for platforms.",
    ),
    **template(
        endpoint="/controller/device-attachment-labels",
        description="Get the list of distinct labels of all device attachments.",
        operation_id="controller_device_attachment_labels",
        response_description="List of distinct device attachment labels.",
    ),
    **template(
        endpoint="/controller/device-custom-field-keys",
        description="Get the list of distinct custom field keys of all devices.",
        operation_id="controller_device_custom_field_keys",
        response_description="List of distinct custom field keys for devices.",
    ),
    **template(
        endpoint="/controller/device-custom-field-values",
        description="Get the list of distinct custom field values of all devices.",
        operation_id="controller_device_custom_field_values",
        response_description="List of distinct custom field values for devices.",
    ),
    **template(
        endpoint="/controller/device-parameter-labels",
        description="Get the list of distinct labels of all device parameters.",
        operation_id="controller_device_parameter_labels",
        response_description="List of distinct labels for device parameters.",
    ),
    **template(
        endpoint="/controller/device-property-labels",
        description="Get the list of distinct labels of all device properties.",
        operation_id="controller_device_property_labels",
        response_description="List of distinct device property labels.",
    ),
    **template(
        endpoint="/controller/device-calibration-action-formulas",
        description="Get the list of distinct formulas of all device calibration actions.",
        operation_id="controller_device_calibration_action_forumlas",
        response_description="List of distinct device calibration action formulas.",
    ),
    **template(
        endpoint="/controller/device-calibration-action-descriptions",
        description="Get the list of distinct descriptions of all device calibration actions.",
        operation_id="controller_device_calibration_action_descriptions",
        response_description="List of distinct device calibration action descriptions.",
    ),
    **template(
        endpoint="/controller/configuration-labels",
        description="Get the list of distinct labels of all configurations.",
        operation_id="controller_configuration_labels",
        response_description="List of distinct labels for configurations.",
    ),
    **template(
        endpoint="/controller/configuration-projects",
        description="Get the list of distinct projects of all configurations.",
        operation_id="controller_configuration_projects",
        response_description="List of distinct projects for configurations.",
    ),
    **template(
        endpoint="/controller/configuration-attachment-labels",
        description="Get the list of distinct labels of all configuration attachments.",
        operation_id="controller_configuration_attachment_labels",
        response_description="List of distinct configuration attachment labels.",
    ),
    **template(
        endpoint="/controller/configuration-parameter-labels",
        description="Get the list of distinct labels of all configuration parameters.",
        operation_id="controller_configuration_parameter_labels",
        response_description="List of distinct labels for configuation parameters.",
    ),
    **template(
        endpoint="/controller/generic-device-action-descriptions",
        description="Get the list of distinct descriptions of all generic device actions.",
        operation_id="controller_generic_device_action_descriptions",
        response_description="List of distinct device action descriptions.",
    ),
    **template(
        endpoint="/controller/generic-platform-action-descriptions",
        description="Get the list of distinct descriptions of all generic platform actions.",
        operation_id="controller_generic_platform_action_descriptions",
        response_description="List of distinct platform action descriptions.",
    ),
    **template(
        endpoint="/controller/generic-configuration-action-descriptions",
        description="Get the list of distinct descriptions of all generic configuration actions.",
        operation_id="controller_generic_configuration_action_descriptions",
        response_description="List of distinct configuration action descriptions.",
    ),
    **template(
        endpoint="/controller/device-software-update-action-descriptions",
        description="Get the list of distinct descriptions of all device software update actions.",
        operation_id="controller_device_software_update_action_descriptions",
        response_description="List of distinct software update action descriptions for devices.",
    ),
    **template(
        endpoint="/controller/device-software-update-action-repository-urls",
        description=(
            "Get the list of distinct repository urls of all "
            "device software update actions."
        ),
        operation_id="controller_device_software_update_action_repository_urls",
        response_description="List of distinct software update action repository urls for devices.",
    ),
    **template(
        endpoint="/controller/platform-software-update-action-descriptions",
        description=(
            "Get the list of distinct descriptions of all "
            "platform software update actions."
        ),
        operation_id="controller_platform_software_update_action_descriptions",
        response_description="List of distinct software update action descriptions for platforms.",
    ),
    **template(
        endpoint="/controller/platform-attachment-labels",
        description="Get the list of distinct labels of all platform attachments.",
        operation_id="controller_platform_attachment_labels",
        response_description="List of distinct platform attachment labels.",
    ),
    **template(
        endpoint="/controller/platform-parameter-labels",
        description="Get the list of distinct labels of all platform parameters.",
        operation_id="controller_platform_parameter_labels",
        response_description="List of distinct labels for platform parameters.",
    ),
    **template(
        endpoint="/controller/platform-software-update-action-repository-urls",
        description=(
            "Get the list of distinct repository urls of all "
            "platform software update actions."
        ),
        operation_id="controller_platform_software_update_action_repository_urls",
        response_description="List of distinct software update action repository urls for platforms.",
    ),
    **template(
        endpoint="/controller/site-buildings",
        description=("Get the list of distinct buildings of all sites"),
        operation_id="controller_site_buildings",
        response_description="List of distinct buildings for sites.",
    ),
    **template(
        endpoint="/controller/site-cities",
        description=("Get the list of distinct cities of all sites"),
        operation_id="controller_site_cities",
        response_description="List of distinct cities for sites.",
    ),
    **template(
        endpoint="/controller/site-countries",
        description=("Get the list of distinct countries of all sites"),
        operation_id="controller_site_countries",
        response_description="List of distinct countries for sites.",
    ),
    **template(
        endpoint="/controller/site-labels",
        description=("Get the list of distinct labels of all sites"),
        operation_id="controller_site_labels",
        response_description="List of distinct labels for sites.",
    ),
    **template(
        endpoint="/controller/site-rooms",
        description=("Get the list of distinct rooms of all sites"),
        operation_id="controller_site_rooms",
        response_description="List of distinct rooms for sites.",
    ),
    **template(
        endpoint="/controller/site-streets",
        description=("Get the list of distinct streets of all sites"),
        operation_id="controller_site_streets",
        response_description="List of distinct streets for sites.",
    ),
    **template(
        endpoint="/controller/site-street-numbers",
        description=("Get the list of distinct street numbers of all sites"),
        operation_id="controller_site_street_numbers",
        response_description="List of distinct street numbers for sites.",
    ),
    **template(
        endpoint="/controller/site-zip-codes",
        description=("Get the list of distinct zip codes of all sites"),
        operation_id="controller_site_zip_codes",
        response_description="List of distinct zip codes for sites.",
    ),
    **template(
        endpoint="/controller/site-attachment-labels",
        description="Get the list of distinct labels of all site attachments.",
        operation_id="controller_site_attachment_labels",
        response_description="List of distinct site attachment labels.",
    ),
    **template(
        endpoint="/controller/configuration-custom-field-keys",
        description="Get the list of distinct configuration custom field keys of all devices.",
        operation_id="controller_configuration_custom_field_keys",
        response_description="List of distinct custom field keys for configurations.",
    ),
    **template(
        endpoint="/controller/configuration-custom-field-values",
        description="Get the list of distinct configuration custom field values of all devices.",
        operation_id="controller_configuration_custom_field_values",
        response_description="List of distinct custom field values for configurations.",
    ),
    **template(
        endpoint="/controller/contact-organizations",
        description="Get the list of distinct organization field values of all contacts.",
        operation_id="controller_contact_organizations",
        response_description="List of distinct organizations.",
    ),
    **template(
        endpoint="/controller/attachment-labels",
        description="Get the list of distinct labels of all attachments.",
        operation_id="controller_attachment_labels",
        response_description="List of distinct attachment labels.",
    ),
    **template(
        endpoint="/controller/keywords",
        description="Get the list of distinct keywords of all devices, platforms, configurations and sites.",
        operation_id="controller_keywords",
        response_description="List of distinct keywords.",
    ),
}
