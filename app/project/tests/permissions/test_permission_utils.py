from unittest.mock import Mock, patch

from project.api.helpers.errors import ConflictError
from project.api.helpers.errors import ServiceIsUnreachableError
from project.api.services.idl_services import Idl
from project.tests.base import BaseTestCase
from requests.exceptions import Timeout, HTTPError

IDL_MOCKED_USER_ACCOUNT = [
    {
        "id": "1000",
        "username": "testuser@ufz.de",
        "administratedPermissionsGroups": ["1"],
        "memberedPermissionsGroups": ["2", "3"],
    }
]


class TestInstituteDecouplingLayerApi(BaseTestCase):
    def test_get_permission_groups_user_not_found(self):
        """Test an empty array from idl"""
        idl_empty_response = []
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = idl_empty_response

            response = Idl().get_all_permission_groups("noUser@ufz.de")
            self.assertEqual(response, [])

    @patch("requests.get")
    def test_get_permission_groups_time_out(self, mock_get):
        """Make sure that error raise (ServiceIsUnreachableError) if IDL not responding."""
        mock_get.side_effect = Timeout
        with self.assertRaises(ServiceIsUnreachableError):
            _ = Idl().get_all_permission_groups("noUser@ufz.de")

    def test_get_all_permission_groups(self):
        """Test data in User account"""
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = IDL_MOCKED_USER_ACCOUNT

            response = Idl().get_all_permission_groups(
                IDL_MOCKED_USER_ACCOUNT[0]["username"]
            )

            self.assertEqual(response.id, "1000")
            self.assertEqual(response.username, IDL_MOCKED_USER_ACCOUNT[0]["username"])
            self.assertEqual(
                IDL_MOCKED_USER_ACCOUNT[0]["administratedPermissionsGroups"],
                response.administrated_permissions_groups,
            )
            self.assertEqual(
                IDL_MOCKED_USER_ACCOUNT[0]["memberedPermissionsGroups"],
                response.membered_permissions_groups,
            )

    def test_get_permission_with_HTTPError_from_idl(self):
        """Test HTTPError from idl """
        with patch("requests.get") as mock_get:
            mock_get.side_effect = HTTPError
            with self.assertRaises(ConflictError):
                _ = Idl().get_all_permission_groups("noUser@ufz.de")
