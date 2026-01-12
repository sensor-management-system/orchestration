# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for getting the permission groups."""


from project import base_url
from project.api.models import PermissionGroup
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestPermissionGroup(BaseTestCase):
    """Tests for the Permission Group Service."""

    url = base_url + "/permission-groups"

    def test_get(self):
        """Ensure it works with a valid jwt."""
        permission_group1 = PermissionGroup(name="group1", entitlement="g1")
        permission_group2 = PermissionGroup(name="group2", entitlement="g2")
        db.session.add_all([permission_group1, permission_group2])
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        self.assertEqual(len(data), 2)
