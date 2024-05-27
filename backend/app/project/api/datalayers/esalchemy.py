# SPDX-FileCopyrightText: 2020 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Classes to help searching in the elasticsearch."""

import csv
import io
from dataclasses import dataclass, field
from typing import List

from flask import current_app, request
from flask_rest_jsonapi.data_layers.alchemy import SqlalchemyDataLayer


@dataclass
class MultiFieldMatchFilter:
    """Class to search for a match in all the fields."""

    query: str
    type_: str = "best_fields"
    fields: List[str] = field(default_factory=lambda: ["*"])
    # The type_ of best_fields is the default value that
    # the elasticsearch uses if no explicit value is given.
    # Ok to search full words, but for substring matches
    # something like 'phrase' should be considered.

    def to_query(self):
        """Convert the filter to a query."""
        result = {
            "multi_match": {
                "query": self.query,
                "type": self.type_,
                "fields": self.fields,
            },
        }
        return result


@dataclass
class MultiFieldWildcardFilter:
    """Class to apply a wildcard filter."""

    value: str
    fields: List[str]

    def to_query(self):
        """Convert the filter to a query."""
        or_parts = []
        for single_field in self.fields:
            single_search = {"wildcard": {single_field: {"value": self.value}}}
            or_parts.append(single_search)
        result = {"bool": {"should": or_parts}}
        return result


class MustNotFilter:
    """Class to represent an inverted filter."""

    def __init__(self, inner_filter):
        """Init the object."""
        self.inner_filter = inner_filter

    def to_query(self):
        """Convert the filter to a query."""
        return {"bool": {"must_not": [self.inner_filter.to_query()]}}

    def __eq__(self, other):
        """Test equality."""
        if not isinstance(other, MustNotFilter):
            return False
        if not self.inner_filter == other.inner_filter:
            return False
        return True

    def __repr__(self):
        """Transform to a string reprentation."""
        return f"MustNotFilter(inner_filter={repr(self.inner_filter)})"


@dataclass
class ExistsFilter:
    """
    Class to represent a filter that checks if any value exists.

    Together with the MustNotFilter we can create checks that a value
    is null or not.
    """

    field: str

    def to_query(self):
        """Convert the filter to a query."""
        return {"exists": {"field": self.field}}


class TermEqualsExactStringFilter:
    """Class to search for an exact string match in the field."""

    def __init__(self, term, value):
        """Init the object."""
        self.term = term
        self.value = value

    def to_query(self):
        """Convert the filter to a query."""
        return {"term": {f"{self.term}": {"value": self.value}}}

    def __eq__(self, other):
        """Test equality."""
        if not isinstance(other, TermEqualsExactStringFilter):
            return False
        if not self.term == other.term:
            return False
        if not self.value == other.value:
            return False
        return True

    def __repr__(self):
        """Transform to a string reprentation."""
        return f"TermEqualsExactStringFilter(term={repr(self.term)},value={repr(self.value)})"


class NestedElementFilterWrapper:
    """
    Wrapper to allow other filtering access to nested fields.

    Example is to access the email field of a contact that is
    associated with a device.
    """

    def __init__(self, path, inner_filter):
        """Init the object."""
        self.path = path
        self.inner_filter = inner_filter

    def to_query(self):
        """Return the es query representation of the filter."""
        return {"nested": {"path": self.path, "query": self.inner_filter.to_query()}}

    def __eq__(self, other):
        """Test equality."""
        if not isinstance(other, NestedElementFilterWrapper):
            return False
        if not self.path == other.path:
            return False
        if not self.inner_filter == other.inner_filter:
            return False
        return True

    def __repr__(self):
        """Transform to a string reprentation."""
        return "".join(
            [
                "NestedElementFilterWrapper(",
                f"path={repr(self.path)}, ",
                f"inner_filter={repr(self.inner_filter)})",
            ]
        )


@dataclass
class TermHasAnyExactFilter:
    """Filter to check for several values of that one must match."""

    term: str
    value: str

    def to_query(self):
        """Return the elasticquery to match any of the values."""
        # ES doesn't differ that much for arrays or scalar values.
        # For the first try, we try to do it like the normal term filter.
        # as in the es it doesn't make that much differnce if term
        # is a scalar or a list field.
        return {"term": {f"{self.term}": {"value": self.value}}}


class TermExactInListFilter:
    """Class to search for an exact string match in the field with multiple values."""

    def __init__(self, term, values):
        """Init the object."""
        self.term = term
        self.values = values

    def to_query(self):
        """Convert the filter to a query."""
        sub_filters = [
            TermEqualsExactStringFilter(term=self.term, value=v) for v in self.values
        ]
        or_filter = OrFilter(sub_filters=sub_filters)
        return or_filter.to_query()

    def __eq__(self, other):
        """Test equality."""
        if not isinstance(other, TermExactInListFilter):
            return False
        if not self.term == other.term:
            return False
        if not self.values == other.values:
            return False
        return True

    def __repr__(self):
        """Transform to a string reprentation."""
        return (
            "TermExactInListFilter(term={repr(self.term)}, values={repr(self.values)})"
        )


class OrFilter:
    """Class to search with multiple filters (and one must match)."""

    def __init__(self, sub_filters):
        """Init the object."""
        self.sub_filters = sub_filters

    def to_query(self):
        """Convert the filter to a query."""
        sub_queries = [f.to_query() for f in self.sub_filters]
        return {"bool": {"should": sub_queries}}

    def __eq__(self, other):
        """Test equality."""
        if not isinstance(other, OrFilter):
            return False
        if not self.sub_filters == other.sub_filters:
            return False
        return True

    def __repr__(self):
        """Transform to a string reprentation."""
        return f"OrFilter(sub_filters={repr(self.sub_filters)})"


class AndFilter:
    """Class to search with multiple filters (all must match)."""

    def __init__(self, sub_filters):
        """Init the object."""
        self.sub_filters = sub_filters

    def to_query(self):
        """Convert the filter to a query."""
        sub_queries = [f.to_query() for f in self.sub_filters]
        return {"bool": {"must": sub_queries}}

    def __eq__(self, other):
        """Test equality."""
        if not isinstance(other, AndFilter):
            return False
        if not self.sub_filters == other.sub_filters:
            return False
        return True

    def __repr__(self):
        """Transform to a string reprentation."""
        return f"AndFilter(sub_filters={repr(self.sub_filters)})"

    def simplify(self):
        """Return an simplified filter if possible (otherwise return yourself)."""
        if len(self.sub_filters) == 1:
            return self.sub_filters[0]
        return self

    @classmethod
    def combine_optionals(cls, filters):
        """Help to deal with None filters but AND like semantic if they are set."""
        not_none_filters = [f for f in filters if f is not None]
        if not_none_filters:
            return AndFilter(not_none_filters).simplify()
        return None


class FilterParser:
    """Class to parse the filter settings."""

    @classmethod
    def wrap_for_nested_elements(cls, name, inner_filter):
        """
        Wrap the main filter in a NestedElementFilterWrapper if necessary.

        In case that we want to filter for a nested field, like
        the email of a contact associated with a device, we need
        to tell the elasticsearch (es) the path to that field.
        This method adds those wrappers as necessary.
        """
        # Say the name is 'abc.def.xyz' or just 'name'.
        # In case of name we don't need any wrapper.
        # But for the other one we do.
        parts = name.split(".")
        # parts would be now ['abc', 'def', 'xyz'] or ['name']
        # We don't care about the last part - for that we don't need
        # to give a path - the es knows that just easliy.
        parts_for_wraper_to_care = parts[:-1]
        # Now, we need the full qualified parts
        # so abc, abc.def
        full_qualified_parts_for_wrapper = []
        for i in range(len(parts_for_wraper_to_care)):
            start_index = 0
            end_index = i + 1
            parts_list = parts_for_wraper_to_care[start_index:end_index]
            parts_joined = ".".join(parts_list)
            full_qualified_parts_for_wrapper.append(parts_joined)

        # Now that we have those, but we have to wrap them
        # in a reversed way.
        # so that the result is: {
        # "abc": {
        #    "abc.def": {
        #        main_filter
        # ...
        result = inner_filter

        for path in reversed(full_qualified_parts_for_wrapper):
            result = NestedElementFilterWrapper(path, result)

        return result

    @classmethod
    def parse(cls, filter_list):
        """Parse the list of filters."""
        if not filter_list:
            return None
        sub_filters = [cls.parse_single_filter(f) for f in filter_list]
        sub_filters = [f for f in sub_filters if f is not None]
        if not sub_filters:
            return None
        if len(sub_filters) == 1:
            return sub_filters[0]
        return AndFilter(sub_filters=sub_filters)

    @classmethod
    def parse_single_filter(cls, filter_dict):
        """Parse a single filter."""
        SUPPORTED_OPS = {
            "eq": lambda name, val: cls.wrap_for_nested_elements(
                name,
                TermEqualsExactStringFilter(term=name, value=val)
                if val is not None
                else MustNotFilter(ExistsFilter(field=name)),
            ),
            "in_": lambda name, val: cls.wrap_for_nested_elements(
                name, TermExactInListFilter(term=name, values=val)
            ),
            "any": lambda name, val: cls.wrap_for_nested_elements(
                name, TermHasAnyExactFilter(term=name, value=val)
            ),
            "ne": lambda name, val: cls.wrap_for_nested_elements(
                name,
                # It is going to be a little bit complex here.
                # In case we use the "ne" with a value of None,
                # then we want the query that makes sure our field exists.
                # Otherwise we want to check that the value that we search
                # for is not the one that we give in the query.
                ExistsFilter(field=name)
                if val is None
                else MustNotFilter(TermEqualsExactStringFilter(term=name, value=val)),
            ),
        }
        # First check if we have a more complex filter
        if "or" in filter_dict.keys():
            sub_filters = [cls.parse_single_filter(f) for f in filter_dict["or"]]
            return OrFilter(sub_filters)
        if "and" in filter_dict.keys():
            sub_filters = [cls.parse_single_filter(f) for f in filter_dict["and"]]
            return AndFilter(sub_filters)
        # Then check if the op syntax is used (name=x, op=eq, val=value)
        op = filter_dict.get("op")
        if op in SUPPORTED_OPS.keys():
            return SUPPORTED_OPS[op](filter_dict["name"], filter_dict["val"])
        # And last, check if we have a simple x:y filter
        if len(filter_dict.keys()) == 1:
            term = [x for x in filter_dict.keys()][0]
            value = filter_dict[term]
            return cls.wrap_for_nested_elements(
                term, TermEqualsExactStringFilter(term=term, value=value)
            )
        return None


class EsQueryBuilder:
    """Builder class for an es query."""

    def __init__(self):
        """Init the object."""
        self.q = None
        self.filters = []

    def with_request_args(self, request_args):
        """Get the settings from the request arguments."""
        self.q = request_args.get("q")
        return self

    def with_filter_args(self, filters):
        """Get the settings from the filters list."""
        self.filters = filters
        return self

    def is_set(self):
        """
        Return true if the es query should be used.

        If false, then we will use the ordinary search.
        """
        if not self.q and not self.filters:
            return False
        return True

    @staticmethod
    def split_query(q):
        """Split the query in those parts that should be searched individually."""
        values = [x.strip() for x in next(csv.reader(io.StringIO(q), delimiter=" "))]
        return values

    def to_filter(self, model):
        """Return the filter out of the settings."""
        sub_filters = []
        if self.q:
            and_filters = []
            parts = self.split_query(self.q)
            idx = 0
            text_search_fields = model.text_search_fields()
            while idx < len(parts):
                part = parts[idx]
                if part == "AND":
                    # Ignore that one. To use and semantics is our default.
                    idx += 1
                elif part == "OR":
                    # We want to support alternatives.
                    if idx + 1 < len(parts) and and_filters:
                        or1 = and_filters[-1]
                        or2 = MultiFieldMatchFilter(
                            query=parts[idx + 1],
                            type_="phrase",
                            fields=text_search_fields,
                        )
                        and_filters[-1] = OrFilter(sub_filters=[or1, or2])
                        idx += 2
                    else:
                        # Nothing to combine => Skip.
                        idx += 1
                else:
                    if part.startswith("-"):
                        and_filters.append(
                            MustNotFilter(
                                MultiFieldMatchFilter(
                                    query=part[1:],
                                    type_="phrase",
                                    fields=text_search_fields,
                                )
                            )
                        )
                    elif "*" in part:
                        and_filters.append(
                            MultiFieldWildcardFilter(
                                value=part, fields=text_search_fields
                            )
                        )
                    else:
                        and_filters.append(
                            MultiFieldMatchFilter(
                                query=part, type_="phrase", fields=text_search_fields
                            )
                        )
                    idx += 1
            sub_filters.append(AndFilter(and_filters).simplify())
        if self.filters:
            sub_filters.append(FilterParser.parse(filter_list=self.filters))
        result = AndFilter(sub_filters).simplify()
        return result


class EsSqlalchemyDataLayer(SqlalchemyDataLayer):
    """Data layer for the elasticsearch (with sqlalchemy under the hood)."""

    REWRITABLE_METHODS = SqlalchemyDataLayer.REWRITABLE_METHODS + ("es_query",)

    def get_pagination_parameter(self, paginate_info):
        """
        Return the parameter for pagination.

        The elasticsearch will care about the pagination, so we
        need all of the parameters.
        """
        size = int(paginate_info.get("size", current_app.config["PAGE_SIZE"]))
        number = int(paginate_info.get("number", 1))

        return {"size": size, "number": number}

    def es_query(self, view_kwargs):
        """
        Return a filter for the view collection.

        This is just a default implementation that doesn't
        filter anything.

        The views (aka list resources) themselves can overwrite
        this method to get the queryset they need.

        This works in combination with the model.search method
        where we send the filters to the elasticsearch.
        """
        return None

    def get_collection(self, qs, view_kwargs, filters=None):
        """
        Return the collection according to the arguments and filters.

        Overloads the original get_collection from the basic
        SqlalchemyDataLayer - and it uses this method as
        fallback in case we don't have elasticsearch available
        or we don't have any argument to search with in elasticsearch.
        """
        # We basically want to extend the search to use elasticsearch
        #
        # if we don't have our elasticsearch available,
        # then we want just to use the basic json api features
        # (filtering, sorting, pagination)
        if current_app.elasticsearch is None:
            return super().get_collection(qs, view_kwargs, filters)

        # All the filter should be used in the search method.
        query_builder = EsQueryBuilder()
        query_builder.with_request_args(request.args)
        if qs.filters:
            query_builder.with_filter_args(qs.filters)

        # Also, if we don't get a search string, we do the very same.
        if not query_builder.is_set():
            return super().get_collection(qs, view_kwargs, filters)

        # now we have a search string, so we want to go with our search logic
        # As in the initial get_collection method we give a hook here.
        self.before_get_collection(qs, view_kwargs)
        es_filter_query = self.es_query(view_kwargs)
        # but as elasticsearch itself cares about pagination, we need
        # to have the sizes & the page number available right now.
        pagination = self.get_pagination_parameter(qs.pagination)
        page = pagination["number"]
        per_page = pagination["size"]

        # Then we run our search.
        search_filter = query_builder.to_filter(self.model)
        if es_filter_query:
            search_filter = AndFilter([search_filter, es_filter_query])
        search_query = search_filter.to_query()

        ordering = []
        if qs.sorting:
            # order can be list of dicts like this:
            # [{"field": "short_name", "order": "asc"}]
            # We need to make it ready for the elasticsearch,
            # which expects it as [{"short_name": "asc"}]
            for entry in qs.sorting:
                ordering.append({entry["field"]: entry["order"]})
        # Elasticsearch handles here filtering, pagination & sorting.
        query, object_count = self.model.search(search_query, page, per_page, ordering)
        # Still we want to include the data if we are asked.
        if getattr(self, "eagerload_includes", True):
            query = self.eagerload_includes(query, qs)

        collection = query.all()

        # And we want to give back our collection.
        collection = self.after_get_collection(collection, qs, view_kwargs)

        return object_count, collection
