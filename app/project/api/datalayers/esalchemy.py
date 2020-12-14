"""Classes to help searching in the elasticsearch."""

from flask_rest_jsonapi.data_layers.alchemy import SqlalchemyDataLayer
from flask import request, current_app


class MultiFieldMatchFilter:
    """Class to search for a match in all the fields."""

    def __init__(self, query):
        """Init the object."""
        self.query = query

    def to_query(self):
        """Convert the filter to a query."""
        return {
            "multi_match": {"query": self.query, "fields": ["*"]},
        }

    def __eq__(self, other):
        """Test equality."""
        if not isinstance(other, MultiFieldMatchFilter):
            return False
        if not self.query == other.query:
            return False
        return True


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

    def simplify(self):
        """Return an simplified filter if possible (otherwise return yourself)."""
        if len(self.sub_filters) == 1:
            return self.sub_filters[0]
        return self


class FilterParser:
    """Class to parse the filter settings."""

    SUPPORTED_OPS = {
        "eq": lambda name, val: TermEqualsExactStringFilter(term=name, value=val),
        "in_": lambda name, val: TermExactInListFilter(term=name, values=val),
    }

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
        # First check if we have a more complex filter
        if "or" in filter_dict.keys():
            sub_filters = [cls.parse_single_filter(f) for f in filter_dict["or"]]
            return OrFilter(sub_filters)
        if "and" in filter_dict.keys():
            sub_filters = [cls.parse_single_filter(f) for f in filter_dict["and"]]
            return AndFilter(sub_filters)
        # Then check if the op syntax is used (name=x, op=eq, val=value)
        op = filter_dict.get("op")
        if op in cls.SUPPORTED_OPS.keys():
            return cls.SUPPORTED_OPS[op](filter_dict["name"], filter_dict["val"])
        # And last, check if we have a simple x:y filter
        if len(filter_dict.keys()) == 1:
            term = [x for x in filter_dict.keys()][0]
            value = filter_dict[term]
            return TermEqualsExactStringFilter(term=term, value=value)
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

    def to_filter(self):
        """Return the filter out of the settings."""
        sub_filters = []
        if self.q:
            sub_filters.append(MultiFieldMatchFilter(query=self.q))
        if self.filters:
            sub_filters.append(FilterParser.parse(filter_list=self.filters))
        return AndFilter(sub_filters).simplify()


class EsSqlalchemyDataLayer(SqlalchemyDataLayer):
    """Data layer for the elasticsearch (with sqlalchemy under the hood)."""

    def get_pagination_parameter(self, paginate_info):
        """
        Return the parameter for pagination.

        The elasticsearch will care about the pagination, so we
        need all of the parameters.
        """
        size = int(paginate_info.get("size", current_app.config["PAGE_SIZE"]))
        number = int(paginate_info.get("number", 1))

        return {"size": size, "number": number}

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

        # but as elasticsearch itself cares about pagination, we need
        # to have the sizes & the page number available right now.
        pagination = self.get_pagination_parameter(qs.pagination)
        page = pagination["number"]
        per_page = pagination["size"]

        # Then we run our search.
        search_filter = query_builder.to_filter()
        search_query = search_filter.to_query()
        query, object_count = self.model.search(search_query, page, per_page)
        # And as Elasticsearch handles pagination, we don't have to care here.
        # Normally same is true for sorting. Elasticsearch sorts by relevance.
        # But in case an explicit sorting is given, we want to support it
        # as well:
        if qs.sorting:
            query = self.sort_query(query, qs.sorting)

        # Still we want to include the data if we are asked.
        if getattr(self, "eagerload_includes", True):
            query = self.eagerload_includes(query, qs)

        collection = query.all()

        # And we want to give back our collection.
        collection = self.after_get_collection(collection, qs, view_kwargs)

        return object_count, collection
