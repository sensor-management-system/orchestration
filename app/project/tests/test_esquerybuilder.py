import unittest

from project.api.datalayers.esalchemy import EsQueryBuilder


class TestEsQueryBuilder(unittest.TestCase):
    """This are the test cases for the es query builder."""

    def test_empty(self):
        """
        Test that the query is not active.

        In case that we don't give any arguments for the elasticsearch
        query, then the query should not be active (so that it is
        clear that the basic search functionality of the json api
        should be used)."""
        builder = EsQueryBuilder()
        is_set = builder.is_set()
        self.assertFalse(is_set)

    def test_with_query_string(self):
        """
        Test with a query string.

        If we give it a simple query string, we want to use our elasticsearch
        query - and we have an idea on how it should look like.
        """
        for q in ["search1", "search2", "something different"]:
            builder = EsQueryBuilder()
            builder.q = q

            is_set = builder.is_set()
            self.assertTrue(is_set)

            query = builder.to_query()
            expected = {"multi_match": {"query": q, "fields": ["*"]}}
            self.assertEqual(query, expected)
