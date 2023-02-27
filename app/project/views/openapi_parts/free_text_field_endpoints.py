"""Openapi docs helper file for the free text endpoints."""


def template(endpoint, description, operation_id):
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
                        }
                    },
                    "401": {"$ref": "#/components/errors/authentification_required"},
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
                    }
                },
                "401": {"$ref": "#/components/errors/authentification_required"},
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
                    }
                },
                "401": {"$ref": "#/components/errors/authentification_required"},
            },
            "description": "Get the list of distinct serial numbers of all devices.",
            "operationId": "controller_device_serial_numbers",
        }
    },
    **template(
        endpoint="/controller/device-short-names",
        description="Get the list of distinct short names of all devices.",
        operation_id="controller_device_short_names",
    ),
    **template(
        endpoint="/controller/device-long-names",
        description="Get the list of distinct long names of all devices.",
        operation_id="controller_device_long_names",
    ),
    **template(
        endpoint="/controller/platform-short-names",
        description="Get the list of distinct short names of all platforms.",
        operation_id="controller_platform_short_names",
    ),
    **template(
        endpoint="/controller/platform-long-names",
        description="Get the list of distinct long names of all platforms.",
        operation_id="controller_platform_long_names",
    ),
    **template(
        endpoint="/controller/device-manufacturer-names",
        description="Get the list of distinct manufacturer names of all devices.",
        operation_id="controller_device_manufacturer_names",
    ),
    **template(
        endpoint="/controller/platform-manufacturer-names",
        description="Get the list of distinct manufacturer names of all platforms.",
        operation_id="controller_platform_manufacturer_names",
    ),
    **template(
        endpoint="/controller/device-custom-field-keys",
        description="Get the list of distinct custom field keys of all devices.",
        operation_id="controller_device_custom_field_keys",
    ),
    **template(
        endpoint="/controller/device-custom-field-values",
        description="Get the list of distinct custom field values of all devices.",
        operation_id="controller_device_custom_field_values",
    ),
    **template(
        endpoint="/controller/device-property-labels",
        description="Get the list of distinct labels of all device properties.",
        operation_id="controller_device_property_labels",
    ),
    **template(
        endpoint="/controller/device-calibration-action-formulas",
        description="Get the list of distinct formulas of all device calibration actions.",
        operation_id="controller_device_calibration_action_forumlas",
    ),
    **template(
        endpoint="/controller/device-calibration-action-descriptions",
        description="Get the list of distinct descriptions of all device calibration actions.",
        operation_id="controller_device_calibration_action_descriptions",
    ),
    **template(
        endpoint="/controller/configuration-labels",
        description="Get the list of distinct labels of all configurations.",
        operation_id="controller_configuration_labels",
    ),
    **template(
        endpoint="/controller/generic-device-action-descriptions",
        description="Get the list of distinct descriptions of all generic device actions.",
        operation_id="controller_generic_device_action_descriptions",
    ),
    **template(
        endpoint="/controller/generic-platform-action-descriptions",
        description="Get the list of distinct descriptions of all generic platform actions.",
        operation_id="controller_generic_platform_action_descriptions",
    ),
    **template(
        endpoint="/controller/generic-configuration-action-descriptions",
        description="Get the list of distinct descriptions of all generic configuration actions.",
        operation_id="controller_generic_configuration_action_descriptions",
    ),
    **template(
        endpoint="/controller/device-software-update-action-descriptions",
        description="Get the list of distinct descriptions of all device software update actions.",
        operation_id="controller_device_software_update_action_descriptions",
    ),
    **template(
        endpoint="/controller/device-software-update-action-repository-urls",
        description=(
            "Get the list of distinct repository urls of all "
            "device software update actions."
        ),
        operation_id="controller_device_software_update_action_repository_urls",
    ),
    **template(
        endpoint="/controller/platform-software-update-action-descriptions",
        description=(
            "Get the list of distinct descriptions of all "
            "platform software update actions."
        ),
        operation_id="controller_platform_software_update_action_descriptions",
    ),
    **template(
        endpoint="/controller/platform-software-update-action-repository-urls",
        description=(
            "Get the list of distinct repository urls of all ",
            "platform software update actions.",
        ),
        operation_id="controller_platform_software_update_action_repository_urls",
    ),
    **template(
        endpoint="/controller/site-buildings",
        description=("Get the list of distinct buildings of all sites"),
        operation_id="controller_site_buildings",
    ),
    **template(
        endpoint="/controller/site-cities",
        description=("Get the list of distinct cities of all sites"),
        operation_id="controller_site_cities",
    ),
    **template(
        endpoint="/controller/site-countries",
        description=("Get the list of distinct countries of all sites"),
        operation_id="controller_site_countries",
    ),
    **template(
        endpoint="/controller/site-labels",
        description=("Get the list of distinct labels of all sites"),
        operation_id="controller_site_labels",
    ),
    **template(
        endpoint="/controller/site-rooms",
        description=("Get the list of distinct rooms of all sites"),
        operation_id="controller_site_rooms",
    ),
    **template(
        endpoint="/controller/site-streets",
        description=("Get the list of distinct streets of all sites"),
        operation_id="controller_site_streets",
    ),
    **template(
        endpoint="/controller/site-street-numbers",
        description=("Get the list of distinct street numbers of all sites"),
        operation_id="controller_site_street_numbers",
    ),
    **template(
        endpoint="/controller/site-zip-codes",
        description=("Get the list of distinct zip codes of all sites"),
        operation_id="controller_site_zip_codes",
    ),
    **template(
        endpoint="/controller/configuration-custom-field-keys",
        description="Get the list of distinct configuration custom field keys of all devices.",
        operation_id="controller_configuration_custom_field_keys",
    ),
    **template(
        endpoint="/controller/configuration-custom-field-values",
        description="Get the list of distinct configuration custom field values of all devices.",
        operation_id="controller_configuration_custom_field_values",
    ),
}
