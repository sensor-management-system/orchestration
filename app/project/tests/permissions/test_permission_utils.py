from unittest.mock import Mock, patch

from flask import request
from requests.exceptions import HTTPError, Timeout

from project.api.auth.permission_utils import (
    allow_only_admin_in_a_permission_group_to_remove_it_from_an_object,
)
from project.api.helpers.errors import ConflictError, ServiceIsUnreachableError
from project.extensions.instances import idl
from project.tests.base import BaseTestCase

IDL_MOCKED_USER_ACCOUNT = [
    {
        "id": "1000",
        "userName": "testuser@ufz.de",
        "administratedPermissionGroups": ["1"],
        "memberedPermissionGroups": ["2", "3"],
    }
]


class TestInstituteDecouplingLayerApi(BaseTestCase):
    def test_get_permission_groups_user_not_found(self):
        """Test an empty array from idl"""
        idl_empty_response = []
        idl.cache_user_account.clear()
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = idl_empty_response

            response = idl.get_all_permission_groups_for_a_user("noUser@ufz.de")
            self.assertEqual(response, None)

    @patch("requests.get")
    def test_get_permission_groups_time_out(self, mock_get):
        """Make sure that error raise (ServiceIsUnreachableError) if IDL not responding."""
        idl.cache_user_account.clear()
        mock_get.side_effect = Timeout
        with self.assertRaises(ServiceIsUnreachableError):
            _ = idl.get_all_permission_groups_for_a_user("noUser@ufz.de")

    def test_get_all_permission_groups(self):
        """Test data in User account"""
        idl.cache_permission_groups.clear()
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = IDL_MOCKED_USER_ACCOUNT

            response = idl.get_all_permission_groups_for_a_user(
                IDL_MOCKED_USER_ACCOUNT[0]["userName"]
            )

            self.assertEqual(response.id, "1000")
            self.assertEqual(response.username, IDL_MOCKED_USER_ACCOUNT[0]["userName"])
            self.assertEqual(
                IDL_MOCKED_USER_ACCOUNT[0]["administratedPermissionGroups"],
                response.administrated_permission_groups,
            )
            self.assertEqual(
                IDL_MOCKED_USER_ACCOUNT[0]["memberedPermissionGroups"],
                response.membered_permission_groups,
            )

    def test_get_permission_with_HTTPError_from_idl(self):
        """Test HTTPError from idl """
        idl.cache_user_account.clear()
        with patch("requests.get") as mock_get:
            mock_get.side_effect = HTTPError
            with self.assertRaises(ConflictError):
                _ = idl.get_all_permission_groups_for_a_user("noUser@ufz.de")


class TestAllowAdminInAPermissionGroupToRemoveItFromAnObject(BaseTestCase):
    """Test allow_only_admin_in_a_permission_group_to_remove_it_from_an_object."""

    def test_with_none(self):
        """
        Test the handling if the existing group ids are None.

        Due to the database handling of the group ids it can be that
        they are None (instead of an empty list for example).
        So we need to handle them as if the list is empty
        and there shouldn't be an error due to transforming
        it in a set somewhere.
        """
        mocked_data = {
            "data": {
                "attributes": {
                    # Just some dummy ids. They really don't matter
                    # for this case.
                    "group_ids": ["1", "2"],
                }
            }
        }
        with patch.object(request, "get_json") as mock:
            mock.return_value = mocked_data
            allow_only_admin_in_a_permission_group_to_remove_it_from_an_object(None)
            # There should be no exception.
