import json

from project.api.models.idl_user import idl_from_dict
from project.tests.base import BaseTestCase


class TestIdlUserGroups(BaseTestCase):
    def test_idl_from_dict(self):
        json_string = '[{"id": 1,"username": "testuser@ufz.de","displayName": "Test User (WKDV)","referencedIri": "/infra/api/v1/accounts/testuser","administratedPermissionsGroups": [2],"memberedPermissionsGroups": [1,3]}]'
        result = idl_from_dict(json.loads(json_string))[0]
        assert "testuser@ufz.de" == result.username
        assert 2 in result.administrated_permissions_groups
        assert 1 in result.membered_permissions_groups
        assert 3 in result.membered_permissions_groups
        assert 2 not in result.membered_permissions_groups
