from flask_rest_jsonapi.data_layers.alchemy import SqlalchemyDataLayer
from flask import request, current_app


class EsQueryBuilder:
    def __init__(self):
        self.q = None

    def with_request_args(self, request_args):
        self.q = request_args.get("q")
        return self

    def is_set(self):
        return self.q is not None

    def to_query(self):
        return {"multi_match": {"query": self.q, "fields": ["*"]}}


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
        # TODO: add other filters here as well.

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
        # Same is true for sorting. Elasticsearch sorts by relevance

        # Still we want to include the data if we are asked.
        if getattr(self, "eagerload_includes", True):
            query = self.eagerload_includes(query, qs)

        collection = query.all()

        # And we want to give back our collection.
        collection = self.after_get_collection(collection, qs, view_kwargs)

        return object_count, collection
