# SPDX-FileCopyrightText: 2020 - 2022
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


def query_index(index, query, page, per_page):
    """Query the index with custom filters & pagination settings."""
    if not current_app.elasticsearch:
        return [], 0
    body = {
        "query": query,
        # the from value is the beginning & starts counting with 0
        "from": (page - 1) * per_page,
        "size": per_page,
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

    current_app.elasticsearch.indices.create(
        index=index,
        aliases=aliases,
        mappings=mappings,
        settings=settings,
    )
