from flask_rest_jsonapi.data_layers.alchemy import SqlalchemyDataLayer
from flask import request, current_app


class MultiFieldMatchFilter:
    def __init__(self, query):
        self.query = query

    def to_query(self):
        return {
            "multi_match": {"query": self.query, "fields": ["*"]},
        }

    def __eq__(self, other):
        if not isinstance(other, MultiFieldMatchFilter):
            return False
        if not self.query == other.query:
            return False
        return True


class TermEqualsExactStringFilter:
    def __init__(self, term, value):
        self.term = term
        self.value = value

    def to_query(self):
        return {"term": {f"{self.term}": {"value": self.value}}}

    def __eq__(self, other):
        if not isinstance(other, TermEqualsExactStringFilter):
            return False
        if not self.term == other.term:
            return False
        if not self.value == other.value:
            return False
        return True


class TermExactInListFilter:
    def __init__(self, term, values):
        self.term = term
        self.values = values

    def to_query(self):
        sub_filters = [
            TermEqualsExactStringFilter(term=self.term, value=v) for v in self.values
        ]
        or_filter = OrFilter(sub_filters=sub_filters)
        return or_filter.to_query()

    def __eq__(self, other):
        if not isinstance(other, TermExactInListFilter):
            return False
        if not self.term == other.term:
            return False
        if not self.values == other.values:
            return False
        return True


class OrFilter:
    def __init__(self, sub_filters):
        self.sub_filters = sub_filters

    def to_query(self):
        sub_queries = [f.to_query() for f in self.sub_filters]
        return {"bool": {"should": sub_queries}}

    def __eq__(self, other):
        if not isinstance(other, OrFilter):
            return False
        if not self.sub_filters == other.sub_filters:
            return False
        return True


class AndFilter:
    def __init__(self, sub_filters):
        self.sub_filters = sub_filters

    def to_query(self):
        sub_queries = [f.to_query() for f in self.sub_filters]
        return {"bool": {"must": sub_queries}}

    def __eq__(self, other):
        if not isinstance(other, AndFilter):
            return False
        if not self.sub_filters == other.sub_filters:
            return False
        return True

    def simplify(self):
        if len(self.sub_filters) == 1:
            return self.sub_filters[0]
        return self


class FilterParser:

    SUPPORTED_OPS = {
        "eq": lambda name, val: TermEqualsExactStringFilter(term=name, value=val),
        "in_": lambda name, val: TermExactInListFilter(term=name, values=val),
    }

    @classmethod
    def parse(cls, filter_list):
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
    def __init__(self):
        self.q = None
        self.filters = []

    def with_request_args(self, request_args):
        self.q = request_args.get("q")
        return self

    def with_filter_args(self, filters):
        self.filters = filters
        return self

    def is_set(self):
        if not self.q and not self.filters:
            return False
        return True

    def to_filter(self):
        sub_filters = []
        if self.q:
            sub_filters.append(MultiFieldMatchFilter(query=self.q))
        if self.filters:
            sub_filters.append(FilterParser.parse(filter_list=self.filters))
        return AndFilter(sub_filters).simplify()


class EsSqlalchemyDataLayer(SqlalchemyDataLayer):
    def get_pagination_parameter(self, paginate_info):
        size = int(paginate_info.get("size", current_app.config["PAGE_SIZE"]))
        number = int(paginate_info.get("number", 1))

        return {"size": size, "number": number}

    def get_collection(self, qs, view_kwargs):
        # We basically want to extend the search to use elasticsearch
        #
        # if we don't have our elasticsearch available,
        # then we want just to use the basic json api features
        # (filtering, sorting, pagination)
        if current_app.elasticsearch is None:
            return super().get_collection(qs, view_kwargs)

        # All the filter should be used in the search method.
        query_builder = EsQueryBuilder()
        query_builder.with_request_args(request.args)
        if qs.filters:
            query_builder.with_filter_args(qs.filters)

        # Also, if we don't get a search string, we do the very same.
        if not query_builder.is_set():
            return super().get_collection(qs, view_kwargs)

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
