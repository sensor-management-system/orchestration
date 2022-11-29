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
