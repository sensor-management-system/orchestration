from project.api.helpers.permission import extract_groups_ids_as_list
from project.tests.base import BaseTestCase


class PermissionMethods(BaseTestCase):
    test_groups_list = [
        {
            "id": 3,
            "username": "testuser@ufz.de",
            "displayName": "Test User (WKDV)",
            "referencedIri": "/infra/api/v1/accounts/testuser",
            "administratedDataprojects": ["/dataprojects/api/dataprojects/2"],
            "memberedDataprojects": [
                "/dataprojects/api/dataprojects/1",
                "/dataprojects/api/dataprojects/3",
            ],
        }
    ]

    def test_get_all_permission_group(self):
        idl_groups = self.test_groups_list[0]["administratedDataprojects"] + self.test_groups_list[0][
            "memberedDataprojects"]
        groups = extract_groups_ids_as_list(idl_groups)
        assert groups == [2, 1, 3]

        idl_groups_admins = self.test_groups_list[0]["administratedDataprojects"]
        admins = extract_groups_ids_as_list(idl_groups_admins)
        assert admins == [2]
