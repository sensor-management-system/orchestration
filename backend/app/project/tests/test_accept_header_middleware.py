# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Some tests for setting the accept header by query paramter."""

from project import base_url
from project.api.models import Device
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestSetAcceptMiddleware(BaseTestCase):
    """Test case for the accept header middleware."""

    def setUp(self):
        """Set some test data up that we can use."""
        super().setUp()
        self.device = Device(
            short_name="some device",
            long_name="longer device name",
            is_public=True,
            is_internal=False,
        )
        db.session.add(self.device)
        db.session.commit()

    def test_csv(self):
        """Ensure that we can query for csv data with the accept query parameter."""
        url = f"{base_url}/devices?accept=text/csv"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csv_data = response.text
        self.assertTrue("short_name,long_name" in csv_data)
        self.assertTrue(f"{self.device.short_name},{self.device.long_name}" in csv_data)

        usual_request = self.client.get(
            f"{base_url}/devices", headers={"Accept": "text/csv"}
        )
        self.assertEqual(usual_request.status_code, 200)
        self.assertEqual(usual_request.text, csv_data)

    def test_usual_json(self):
        """Ensure that our routes stay with their defaults (json:api)."""
        url = f"{base_url}/devices"
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        data = response.json["data"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["attributes"]["short_name"], self.device.short_name)
