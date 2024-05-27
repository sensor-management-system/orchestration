# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests the dictutils."""

from unittest import TestCase

from project.api.helpers import dictutils


class TestDictFromKvList(TestCase):
    """Test the dict_from_kv_list function."""

    def test_empty(self):
        """Ensure it works with an empty list."""
        result = dictutils.dict_from_kv_list([])
        self.assertEqual(result, {})

    def test_two_element_list(self):
        """Ensure we return a proper dict for an two element list."""
        result = dictutils.dict_from_kv_list(["a", "b"])
        self.assertEqual(result, {"a": "b"})

    def test_four_element_list(self):
        """Ensure we can use longer lists too."""
        result = dictutils.dict_from_kv_list(["a", "b", "c", "d"])
        self.assertEqual(result, {"a": "b", "c": "d"})

    def test_doubled_keys(self):
        """Ensure we can use longer lists too."""
        result = dictutils.dict_from_kv_list(["a", "b", "a", "d"])
        self.assertEqual(result, {"a": "d"})

    def test_odd_number_of_elements_in_the_list(self):
        """Ensure we only use the keys we have values for."""
        result = dictutils.dict_from_kv_list(["a", "b", "d"])
        self.assertEqual(result, {"a": "b"})
