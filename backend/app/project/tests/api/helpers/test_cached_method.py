# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Some test classes for the cached_method decorator."""
import operator

from cachetools import TTLCache

from project.api.helpers.cached_method import cached_method
from project.tests.base import BaseTestCase


class FakeIdl:
    """Fake implementation to test basic caching."""

    def __init__(self):
        """Init the object."""
        self.idx = 0
        self.cache = TTLCache(maxsize=100, ttl=1000)

    @cached_method(operator.attrgetter("cache"))
    def get_all_permission_groups_for_a_user(self, user_subject):
        """Return a dict with user information."""
        possible_group_names = ["TERENO", "MOSES", "ELTER", "RIESGOS", "EPOS", "MOSAIC"]
        group = possible_group_names[self.idx]
        self.idx = (self.idx + 1) % len(possible_group_names)
        return dict(name=user_subject, groups=[group])


class FakeIdlSkipCache:
    """Fake implementation with the option to invalidate the cache key."""

    def __init__(self):
        """Init the object."""
        self.idx = 0
        self.cache = TTLCache(maxsize=100, ttl=1000)

    @cached_method(operator.attrgetter("cache"), skip_argument={"cache": "skip"})
    def get_all_permission_groups_for_a_user(self, user_subject):
        """
        Return a dict with user information.

        with cache="skip" argument we can ignore a current cache entry.
        """
        possible_group_names = ["TERENO", "MOSES", "ELTER", "RIESGOS", "EPOS", "MOSAIC"]
        group = possible_group_names[self.idx]
        self.idx = (self.idx + 1) % len(possible_group_names)
        return dict(name=user_subject, groups=[group])


class TestCachedMethod(BaseTestCase):
    """Test class for the cached_method decorator."""

    def test_usage_as_for_cachetools_cachedmethod(self):
        """Ensure we can use it as the cachedmethod function from cachetools."""
        idl = FakeIdl()
        mmorgner_user1 = idl.get_all_permission_groups_for_a_user("mmorgner")
        self.assertEqual(mmorgner_user1["groups"], ["TERENO"])

        nbck_user1 = idl.get_all_permission_groups_for_a_user("nbck")
        self.assertEqual(nbck_user1["groups"], ["MOSES"])

        tschnicke_user1 = idl.get_all_permission_groups_for_a_user("ELTER")
        self.assertEqual(tschnicke_user1["groups"], ["ELTER"])

        nbck_user2 = idl.get_all_permission_groups_for_a_user("nbck")
        self.assertEqual(nbck_user2["groups"], ["MOSES"])

    def test_invalidate(self):
        """Ensure we can invalidate our current cache values."""
        idl = FakeIdlSkipCache()
        mmorgner_user1 = idl.get_all_permission_groups_for_a_user("mmorgner")
        self.assertEqual(mmorgner_user1["groups"], ["TERENO"])

        nbck_user1 = idl.get_all_permission_groups_for_a_user("nbck")
        self.assertEqual(nbck_user1["groups"], ["MOSES"])

        tschnicke_user1 = idl.get_all_permission_groups_for_a_user("ELTER")
        self.assertEqual(tschnicke_user1["groups"], ["ELTER"])

        nbck_user2 = idl.get_all_permission_groups_for_a_user("nbck")
        self.assertEqual(nbck_user2["groups"], ["MOSES"])

        nbck_user3 = idl.get_all_permission_groups_for_a_user("nbck", cache="skip")
        self.assertEqual(nbck_user3["groups"], ["RIESGOS"])

        mmorgner_user2 = idl.get_all_permission_groups_for_a_user("mmorgner")
        self.assertEqual(mmorgner_user2["groups"], ["TERENO"])

        nbck_user4 = idl.get_all_permission_groups_for_a_user("nbck")
        self.assertEqual(nbck_user4["groups"], ["RIESGOS"])
