from flask import current_app


# mostly from here:
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search
def add_to_index(index, model, payload):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        body={
            "query": query,
            # the from value is the beginning & starts counting with 0
            "from": (page - 1) * per_page,
            "size": per_page,
        },
    )
    ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]
    return ids, search["hits"]["total"]["value"]
