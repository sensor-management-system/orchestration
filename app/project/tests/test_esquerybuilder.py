import unittest

from project.api.datalayers.esalchemy import (
    EsQueryBuilder,
    MultiFieldMatchFilter,
    TermEqualsExactStringFilter,
    TermExactInListFilter,
    OrFilter,
    AndFilter,
    FilterParser,
)


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

        If we give it a simple query string, we want it to be active.
        And we want to have an MultiFieldMatchFilter.
        """
        for q in ["search1", "search2", "something different"]:
            builder = EsQueryBuilder()
            builder.q = q

            is_set = builder.is_set()
            self.assertTrue(is_set)

            used_filter = builder.to_filter()
            expected_filter = MultiFieldMatchFilter(query=q)

            self.assertEqual(used_filter, expected_filter)

    def test_fill_query_string_from_request_args(self):
        """
        Test that we can set the query string from the request arguments.

        Given the pure request arguments, we should be able to fill
        our query string property.
        """
        for q in ["search3", "search4", "something very different"]:
            builder = EsQueryBuilder()
            request_args = {}
            request_args["q"] = q
            builder.with_request_args(request_args)

            self.assertEqual(builder.q, q)

    def test_with_filter(self):
        """
        Test with a json api filter.

        As no query string is given it should just use the
        TermEqualsExactStringFilter.
        """
        json_api_filter = {"short_name": "boeken"}
        builder = EsQueryBuilder()
        builder.filters.append(json_api_filter)

        is_set = builder.is_set()
        self.assertTrue(is_set)

        used_filter = builder.to_filter()
        expected_filter = TermEqualsExactStringFilter(term="short_name", value="boeken")

        self.assertEqual(used_filter, expected_filter)

    def test_fill_filter_from_filter_list(self):
        """
        Test filling the filter list from a given list.

        The given list comes from the json api.
        """
        json_api_filters = [{"short_name": "boeken"}]
        builder = EsQueryBuilder()

        self.assertEqual(builder.filters, [])

        builder.with_filter_args(json_api_filters)

        self.assertEqual(builder.filters, json_api_filters)

    def test_query_and_json_api_filter(self):
        """
        Test with both the query and the json api filter.

        Must make sure that both are considered to be fullfilled.
        """
        builder = EsQueryBuilder()
        builder.q = "Boeken"  # Search on all the fields
        builder.filters.append({"short_name": "boeken"})

        es_filter = builder.to_filter()
        expected = AndFilter(
            [
                MultiFieldMatchFilter(query="Boeken"),
                TermEqualsExactStringFilter(term="short_name", value="boeken"),
            ]
        )
        self.assertEqual(es_filter, expected)


class TestMultiMatchStringFilter(unittest.TestCase):
    """
    This are the tests for the MultiMatchStringFilter.

    The filter is used to search for a string (with full es support)
    in all the fields.
    """

    def test_to_query(self):
        """Test the query generation for the filter."""
        for q in ["search1", "search2", "something different"]:
            multi_match_filter = MultiFieldMatchFilter(query=q)
            es_query = multi_match_filter.to_query()
            expected = {"multi_match": {"query": q, "fields": ["*"]}}
            self.assertEqual(es_query, expected)

    def test_eq(self):
        filter1 = MultiFieldMatchFilter(query="a")
        filter2 = MultiFieldMatchFilter(query="a")
        filter3 = MultiFieldMatchFilter(query="b")

        self.assertEqual(filter1, filter2)
        self.assertNotEqual(filter1, filter3)
        self.assertNotEqual(filter1, None)


class TestTermEqualsExactStringFilter(unittest.TestCase):
    """
    This are the tests for the TermEqualsExactStringFilter.

    This filter is used to match exactly the term without further
    changes in the search term.
    """

    def test_to_query(self):
        """Test the query generation for the filter."""
        terms = {"field1": "value1", "field2": "value2"}
        for term, value in terms.items():
            term_equals_filter = TermEqualsExactStringFilter(term=term, value=value)
            es_query = term_equals_filter.to_query()
            expected = {"bool": {f"{term}": {"value": value}}}
            self.assertEqual(es_query, expected)

    def test_eq(self):
        filter1 = TermEqualsExactStringFilter(term="term1", value="value1")
        filter2 = TermEqualsExactStringFilter(term="term1", value="value1")
        filter3 = TermEqualsExactStringFilter(term="term2", value="value1")
        filter4 = TermEqualsExactStringFilter(term="term1", value="value2")

        self.assertEqual(filter1, filter2)
        self.assertNotEqual(filter1, filter3)
        self.assertNotEqual(filter1, filter4)
        self.assertNotEqual(filter1, None)


class TestTermExactInListFilter(unittest.TestCase):
    """
    This are the tests for the TermExactInListFilter.

    This filter is used to match one of the terms in the list.
    """

    def test_to_query(self):
        terms = {
            "field1": ["value1", "value2", "someother value"],
            "field2": ["x", "y", "some loonger element", "and a forth value"],
        }
        for term, values in terms.items():
            term_in_filter = TermExactInListFilter(term=term, values=values)
            es_query = term_in_filter.to_query()

            expected_should_array = [
                {"bool": {f"{term}": {"value": v}}} for v in values
            ]
            expected = {"bool": {"should": expected_should_array}}

            self.assertEqual(es_query, expected)

    def test_eq(self):
        filter1 = TermExactInListFilter(term="term1", values=["val1", "val2"])
        filter2 = TermExactInListFilter(term="term1", values=["val1", "val2"])
        filter3 = TermExactInListFilter(term="term2", values=["val1", "val2"])
        filter4 = TermExactInListFilter(term="term1", values=["val1"])

        self.assertEqual(filter1, filter2)
        self.assertNotEqual(filter1, filter3)
        self.assertNotEqual(filter1, filter4)
        self.assertNotEqual(filter1, None)


class TestOrFilter(unittest.TestCase):
    """
    This are the tests for the OrFilter.

    This filter is used to match in one of the sub filters.
    """

    def test_to_query(self):
        filter1 = TermEqualsExactStringFilter(term="field1", value="value1")
        filter2 = TermEqualsExactStringFilter(term="field2", value="value2")

        or_filter = OrFilter(sub_filters=[filter1, filter2])
        es_query = or_filter.to_query()

        expected = {
            "bool": {
                "should": [
                    {"bool": {"field1": {"value": "value1"}}},
                    {"bool": {"field2": {"value": "value2"}}},
                ]
            }
        }

        self.assertEqual(es_query, expected)

    def test_eq(self):
        filter1 = OrFilter([TermEqualsExactStringFilter(term="term", value="value")])
        filter2 = OrFilter([TermEqualsExactStringFilter(term="term", value="value")])
        filter3 = OrFilter([TermExactInListFilter(term="term", values=["value"])])
        filter4 = OrFilter(
            [
                TermEqualsExactStringFilter(term="term", value="value"),
                TermEqualsExactStringFilter(term="term", value="value"),
            ]
        )

        self.assertEqual(filter1, filter2)
        self.assertNotEqual(filter1, filter3)
        self.assertNotEqual(filter1, filter4)
        self.assertNotEqual(filter1, None)


class TestAndFilter(unittest.TestCase):
    """
    This are the test cases for the AndFilter.

    This filter is used to match all of the sub filters.
    """

    def test_to_query(self):
        filter1 = TermEqualsExactStringFilter(term="field1", value="value1")
        filter2 = TermEqualsExactStringFilter(term="field2", value="value2")

        and_filter = AndFilter(sub_filters=[filter1, filter2])
        es_query = and_filter.to_query()

        expected = {
            "bool": {
                "must": [
                    {"bool": {"field1": {"value": "value1"}}},
                    {"bool": {"field2": {"value": "value2"}}},
                ]
            }
        }

        self.assertEqual(es_query, expected)

    def test_eq(self):
        filter1 = AndFilter([TermEqualsExactStringFilter(term="term", value="value")])
        filter2 = AndFilter([TermEqualsExactStringFilter(term="term", value="value")])
        filter3 = AndFilter([TermExactInListFilter(term="term", values=["value"])])
        filter4 = AndFilter(
            [
                TermEqualsExactStringFilter(term="term", value="value"),
                TermEqualsExactStringFilter(term="term", value="value"),
            ]
        )

        self.assertEqual(filter1, filter2)
        self.assertNotEqual(filter1, filter3)
        self.assertNotEqual(filter1, filter4)
        self.assertNotEqual(filter1, None)


class TestFilterParser(unittest.TestCase):
    """
    This are the test for the FilterParser.

    This parser is used to transform a filter from the
    json api and transform it to one of our filter classes.
    """

    def test_parse_empty(self):
        filter_raw = []
        output_filter = FilterParser.parse(filter_raw)
        self.assertIsNone(output_filter)

    def test_parse_eq(self):
        filter_raw = [{"name": "manufacturer_name", "op": "eq", "val": "Campbell"}]
        output_filter = FilterParser.parse(filter_raw)

        expected = TermEqualsExactStringFilter(
            term="manufacturer_name", value="Campbell"
        )
        self.assertEqual(output_filter, expected)

    def test_parse_in(self):
        filter_raw = [{"name": "manufacturer_name", "op": "in_", "val": ["Campbell"]}]
        output_filter = FilterParser.parse(filter_raw)

        expected = TermExactInListFilter(term="manufacturer_name", values=["Campbell"])
        self.assertEqual(output_filter, expected)

    def test_parse_or_filter(self):
        filter_raw = [
            {
                "or": [
                    {"name": "manufacturer_name", "op": "in_", "val": ["Campbell"]},
                    {
                        "name": "manufacturer_uri",
                        "op": "in_",
                        "val": ["manufacturer/campbell"],
                    },
                ]
            }
        ]

        output_filter = FilterParser.parse(filter_raw)

        expected = OrFilter(
            sub_filters=[
                TermExactInListFilter(term="manufacturer_name", values=["Campbell"]),
                TermExactInListFilter(
                    term="manufacturer_uri", values=["manufacturer/campbell"]
                ),
            ]
        )

        self.assertEqual(output_filter, expected)

    def test_parse_implicit_and_filter(self):
        filter_raw = [
            {"name": "manufacturer_name", "op": "in_", "val": ["Campbell"]},
            {"name": "manufacturer_uri", "op": "in_", "val": ["manufacturer/campbell"]},
        ]

        output_filter = FilterParser.parse(filter_raw)

        expected = AndFilter(
            sub_filters=[
                TermExactInListFilter(term="manufacturer_name", values=["Campbell"]),
                TermExactInListFilter(
                    term="manufacturer_uri", values=["manufacturer/campbell"]
                ),
            ]
        )

        self.assertEqual(output_filter, expected)

    def test_parse_explicit_and_filter(self):
        filter_raw = [
            {
                "and": [
                    {"name": "manufacturer_name", "op": "in_", "val": ["Campbell"]},
                    {
                        "name": "manufacturer_uri",
                        "op": "in_",
                        "val": ["manufacturer/campbell"],
                    },
                ]
            }
        ]
        output_filter = FilterParser.parse(filter_raw)

        expected = AndFilter(
            sub_filters=[
                TermExactInListFilter(term="manufacturer_name", values=["Campbell"]),
                TermExactInListFilter(
                    term="manufacturer_uri", values=["manufacturer/campbell"]
                ),
            ]
        )

        self.assertEqual(output_filter, expected)

    def test_parse_simple_field(self):
        filter_raw = [{"manufacturer_name": "Campbell"}]
        output_filter = FilterParser.parse(filter_raw)

        expected = TermEqualsExactStringFilter(
            term="manufacturer_name", value="Campbell"
        )
        self.assertEqual(output_filter, expected)
