# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

from project.extensions.idl.models import permission_group
from project.tests.base import BaseTestCase


class TestIdlPermissionGroups(BaseTestCase):
    def test_idl_from_dict(self):
        list_of_permission_groups = [
            {
                "id": "1",
                "name": "Test1",
                "description": "",
                "admins": ["1", "2"],
                "members": ["3"],
            },
            {
                "id": "2",
                "name": "Test2",
                "description": "",
                "admins": ["11", "12"],
                "members": ["13"],
            },
        ]
        result = permission_group.permission_groups_from_list_of_dicts(
            list_of_permission_groups
        )
        first_permission_group = result[0].to_dict()
        second_permission_group = result[1].to_dict()
        assert isinstance(result[0], permission_group.PermissionGroup)
        assert "Test1" == first_permission_group["attributes"]["name"]
        assert "admins" not in first_permission_group["attributes"]
        assert "members" not in first_permission_group["attributes"]

        assert "Test2" == second_permission_group["attributes"]["name"]
        assert "admins" not in second_permission_group["attributes"]
        assert "members" not in second_permission_group["attributes"]
