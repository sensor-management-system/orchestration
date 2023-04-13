# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from project.extensions.idl.models import user_account
from project.tests.base import BaseTestCase


class TestIdlUserGroups(BaseTestCase):
    def test_idl_from_dict(self):

        json_string = {
            "id": "1",
            "userName": "testuser@ufz.de",
            "administratedPermissionGroups": ["2"],
            "memberedPermissionGroups": ["1", "3"],
        }
        result = user_account.idl_from_dict(json_string)
        assert "testuser@ufz.de" == result.username
        assert "2" in result.administrated_permission_groups
        assert "1" in result.membered_permission_groups
        assert "3" in result.membered_permission_groups
        assert "2" not in result.membered_permission_groups
