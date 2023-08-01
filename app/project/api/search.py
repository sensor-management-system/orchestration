# SPDX-FileCopyrightText: 2020 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""
Functions to work with the full text search.

You may look at
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search
after most of the source code here was adapted.
"""

from flask import current_app


def add_to_index(index, model, payload):
    """Add an entry to the index in the full text search."""
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.index(index=index, id=model.id, document=payload)


def remove_from_index(index, model):
    """Remove an entry from the index in the full text search."""
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page, ordering=None):
    """
    Query the index with custom filters & pagination settings.

    Ordering is optional as in any case we sort by the score first.
    Everthing else comes as secondary criteria.
    """
    if not current_app.elasticsearch:
        return [], 0
    sort = ["_score"]
    if ordering:
        for entry in ordering:
            sort.append(entry)
    body = {
        "query": query,
        # the from value is the beginning & starts counting with 0
        "from": (page - 1) * per_page,
        "size": per_page,
        "sort": sort,
    }
    search = current_app.elasticsearch.search(
        index=index,
        **body,
    )
    ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]
    return ids, search["hits"]["total"]["value"]


def remove_index(index):
    """Remove an index for the full text search."""
    if not current_app.elasticsearch:
        return
    # if we don't have an index, it is fine
    current_app.elasticsearch.indices.delete(index=index, ignore_unavailable=True)


def create_index(index, payload):
    """Create an index for the full text search."""
    if not current_app.elasticsearch:
        return
    aliases = payload.get("aliases", {})
    mappings = payload.get("mappings", {})
    settings = payload.get("settings", {})

    if "mapping" not in settings.keys():
        settings["mapping"] = {}
    if "total_fields" not in settings["mapping"].keys():
        settings["mapping"]["total_fields"] = {}
    # As we have more and more fields (and quite a lot of ngram levels)
    # we need to increase the limit of total fields for the index.
    settings["mapping"]["total_fields"]["limit"] = 2000

    current_app.elasticsearch.indices.create(
        index=index,
        aliases=aliases,
        mappings=mappings,
        settings=settings,
    )
