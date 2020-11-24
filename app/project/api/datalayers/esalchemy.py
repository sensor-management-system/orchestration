from flask_rest_jsonapi.data_layers.alchemy import SqlalchemyDataLayer
from flask import request, current_app


def to_term(name, value):
    return {"term": {f"{name}": {"value": value}}}


def to_es(jsonapi):
    if "or" in jsonapi.keys():
        parts = jsonapi["or"]
        terms = [to_es(part) for part in parts]
        return {
            "bool": {
                # should => one of the elements must be fulfilled
                # which is exactly the "or"
                "should": terms,
            }
        }
    op = jsonapi["op"]
    if op == "in_":
        values = jsonapi["val"]
        name = jsonapi["name"]
        terms = [to_term(name, val) for val in values]
        return {
            "bool": {
                # Again we use the should to have one of the clauses
                # fulfilled. In this time we check equality for each of
                # the cases
                "should": terms,
            }
        }
    elif op == "eq":
        value = jsonapi["val"]
        name = jsonapi["name"]
        return {"bool": to_term(name, value)}


"""
def test_one_manufacturer_name():
    for value in ['Campell', 'Someother']:
        jsonapi = {'name': 'manufacturer_name', 'op': 'eq', 'val': value}
        output = to_es(jsonapi)

        expected = {
            'bool': {
                'term': {
                    'manufacturer_name': {
                        'value': value,
                    }
                }
            }
        }

        assert output == expected

def test_one_manufacturer_uri():
    for value in ['uri1', 'uri2']:
        jsonapi = {'name': 'manufacturer_uri', 'op': 'eq', 'val': value}
        output = to_es(jsonapi)

        expected = {
            'bool': {
                'term': {
                    'manufacturer_uri': {
                        'value': value,
                    }
                }
            }
        }

        assert output == expected


def test_two_manufacturer_name():
    manufacturers = ['Campell', 'Someother']
    jsonapi = {'name': 'manufacturer_name', 'op': 'in_', 'val': manufacturers}
    output = to_es(jsonapi)

    expected = {
        'bool': {
            'should': [
                {
                    'term': {
                        'manufacturer_name': {
                            'value': manufacturers[0],
                        },
                    },
                },
                {
                    'term': {
                        'manufacturer_name': {
                            'value': manufacturers[1]
                        },
                    },
                },
           ]
        }
    }
    assert output == expected
def test_two_manufacturer_uris():
    manufacturers = ['uri1', 'uri2']
    jsonapi = {'name': 'manufacturer_uri', 'op': 'in_', 'val': manufacturers}
    output = to_es(jsonapi)

    expected = {
        'bool': {
            'should': [
                {
                    'term': {
                        'manufacturer_uri': {
                            'value': manufacturers[0],
                        },
                    },
                },
                {
                    'term': {
                        'manufacturer_uri': {
                            'value': manufacturers[1]
                        },
                    },
                },
           ]
        }
    }
    assert output == expected

def test_manufacturer_name_or_uri():
    manufacturers = ['Campell', 'Someother']
    part_names = {'name': 'manufacturer_name', 'op': 'in_', 'val': manufacturers}
    manufacturer_uris = ['uri1', 'uri2']
    part_uris = {'name': 'manufacturer_uri', 'op': 'in_', 'val': manufacturer_uris}
    part_or = {'or': [part_names, part_uris]}

    expected = {
        'bool': {
            'should': [
                {
                    'bool': {
                        'should': [
                            {
                                'term': {
                                    'manufacturer_name': {
                                        'value': manufacturers[0],
                                    },
                                },
                            },
                            {
                                'term': {
                                    'manufacturer_name': {
                                        'value': manufacturers[1]
                                    },
                                },
                            },
                        ]
                    }
                },
                {
                    'bool': {
                        'should': [
                            {
                                'term': {
                                    'manufacturer_uri': {
                                        'value': manufacturer_uris[0],
                                    },
                                },
                            },
                            {
                                'term': {
                                    'manufacturer_uri': {
                                        'value': manufacturer_uris[1]
                                    },
                                },
                            },
                        ]
                    }
                }
           ]
        }
    }
    output = to_es(part_or)
    assert output == expected

"""


class EsQueryBuilder:
    def __init__(self):
        self.q = None
        self.terms = None

    def with_request_args(self, request_args):
        self.q = request_args.get("q")
        return self

    def with_filter_args(self, filters):
        # How does the filters look like?
        #  [
        #    {
        #      'or': [
        #        {
        #          'name': 'manufacturer_name',
        #          'op': 'in_',
        #          'val': ['Campbell']
        #        },
        #        {
        #          'name': 'manufacturer_uri',
        #          'op': 'in_',
        #          'val': ['manufacturer/Campbell']
        #        }
        #      ]
        #    }
        #  ]
        self.terms = to_es(filters)
        return self

    def is_set(self):
        return self.q is not None or self.terms is not None

    def to_query(self):
        # TODO: write real tests for this
        # if I have a query string then I want it to be used
        # if I additionally have a filter, then this filter should be used
        # as well (both must)
        # however the filter can be quite complex regarding its inner structure
        if self.q:
            if self.terms:
                return {
                    "bool": {
                        "must": [
                            {"multi_match": {"query": self.q, "fields": ["*"]}},
                            {"bool": self.terms["bool"]},
                        ]
                    }
                }
            else:
                return {
                    "multi_match": {"query": self.q, "fields": ["*"]},
                }
        else:
            return {"bool": self.terms["bool"]}


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
        query, object_count = self.model.search(
            query_builder.to_query(), page, per_page
        )
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
