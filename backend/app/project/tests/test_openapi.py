# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the openapi endpoints."""

from project import base_url
from project.tests.base import BaseTestCase


class TestOpenapiHtml(BaseTestCase):
    """Test case that we see the openapi."""

    url = base_url + "/openapi"

    def test_get(self):
        """Ensure that we can get the page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestOpenapiJson(BaseTestCase):
    """Test case that we can work with the openapi."""

    url = base_url + "/openapi.json"

    def test_get(self):
        """Ensure that we can get our openapi payload."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # And ensure we can parse it as json.
        _ = response.json

    def test_has_device_list_endpoint(self):
        """Ensure that we have the endpoint for the devices."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        paths = data.get("paths", {})
        self.assertTrue("/devices" in paths.keys())

    def test_has_userinfo_endpoint(self):
        """Ensure that we have the endpoint for the userinfo."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        paths = data.get("paths", {})
        self.assertTrue("/user-info" in paths.keys())

    def test_list_endpoints_have_page_number_and_page_size_parameter(self):
        """Ensure that we have page size & page number parameters for list endpoints."""
        paths_that_need_to_have_page_parameters = [
            "/configuration-attachments",
            "/configuration-contact-roles",
            "/configuration-customfields",
            "/configuration-parameter-value-change-actions",
            "/configuration-parameters",
            "/configurations",
            "/contacts",
            "/customfields",
            "/datastream-links",
            "/device-attachments",
            "/device-calibration-actions",
            "/device-calibration-attachments",
            "/device-contact-roles",
            "/device-mount-actions",
            "/device-parameter-value-change-actions",
            "/device-parameters",
            "/device-properties",
            "/device-property-calibrations",
            "/device-software-update-action-attachments",
            "/device-software-update-actions",
            "/devices",
            "/dynamic-location-actions",
            "/generic-configuration-actions",
            "/generic-configuration-action-attachments",
            "/generic-device-action-attachments",
            "/generic-device-actions",
            "/generic-platform-action-attachments",
            "/generic-platform-actions",
            "/platform-attachments",
            "/platform-contact-roles",
            "/platform-mount-actions",
            "/platform-parameter-value-change-actions",
            "/platform-parameters",
            "/platform-software-update-action-attachments",
            "/platform-software-update-actions",
            "/platforms",
            "/site-attachments",
            "/site-contact-roles",
            "/sites",
            "/static-location-actions",
            "/tsm-endpoints",
        ]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json
        paths = data.get("paths", {})

        used_page_size_parameter_reference = False
        used_page_number_parameter_reference = False

        for path in paths_that_need_to_have_page_parameters:
            self.assertIn(path, paths.keys())
            specific_methods = paths[path]
            has_page_size = False
            has_page_number = False
            parameters = specific_methods["get"].get("parameters", [])
            self.assertTrue(parameters, f"{path} has get parameters")

            for parameter in parameters:
                # In allmost all of the cases, we have here the
                # references to the page_size and page_number parameters.
                if parameter == {"$ref": "#/components/parameters/page_size"}:
                    has_page_size = True
                    used_page_size_parameter_reference = True
                if parameter == {"$ref": "#/components/parameters/page_number"}:
                    has_page_number = True
                    used_page_number_parameter_reference = True
                # We may can add other checks here, but we don't have to.

            self.assertTrue(has_page_size, f"{path} has page[size]")
            self.assertTrue(has_page_number, f"{path} has page[number]")

        if used_page_size_parameter_reference:
            page_size_parameter = data["components"]["parameters"]["page_size"]
            self.assertEqual(page_size_parameter["name"], "page[size]")
            self.assertEqual(page_size_parameter["in"], "query")
            self.assertEqual(page_size_parameter["required"], False)
            self.assertEqual(page_size_parameter["schema"]["type"], "integer")
            self.assertEqual(page_size_parameter["schema"]["default"], 30)

        if used_page_number_parameter_reference:
            page_number_parameter = data["components"]["parameters"]["page_number"]
            self.assertEqual(page_number_parameter["name"], "page[number]")
            self.assertEqual(page_number_parameter["in"], "query")
            self.assertEqual(page_number_parameter["required"], False)
            self.assertEqual(page_number_parameter["schema"]["type"], "integer")
            self.assertEqual(page_number_parameter["schema"]["default"], 1)
