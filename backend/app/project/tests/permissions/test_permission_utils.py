# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for some util functions to handle permissions."""

from unittest.mock import Mock, patch

from requests.exceptions import HTTPError, Timeout

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
    """Test to get information from the idl."""

    def test_get_permission_groups_user_not_found(self):
        """Test an empty array from idl."""
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
        """Test data in User account."""
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
        """Test HTTPError from idl."""
        idl.cache_user_account.clear()
        with patch("requests.get") as mock_get:
            mock_get.side_effect = HTTPError
            with self.assertRaises(ConflictError):
                _ = idl.get_all_permission_groups_for_a_user("noUser@ufz.de")
