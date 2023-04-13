# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for getting the permission groups."""

from unittest import skipIf

from flask import current_app

from project import base_url
from project.tests.base import BaseTestCase


class TestPermissionGroup(BaseTestCase):
    """Tests for the Permission Group Service."""

    url = base_url + "/permission-groups"

    @skipIf(
        not current_app.config["IDL_URL"],
        "will not work without idl url configuration.",
    )
    def test_get(self):
        """Ensure it works with a valid jwt."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        # This will contain data if it can connect to an
        # instance of the idl with some data.
        # So this is a real request here.
        # If the IDL is unavailable, or just empty
        # it will fail here.
        self.assertNotEqual(len(data), 0)
