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
