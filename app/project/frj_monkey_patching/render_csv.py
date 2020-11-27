"""Modifications: Adopted form Custom content negotiation #171 ( miLibris /
flask-rest-jsonapi )"""
from csv import DictWriter
from io import StringIO

from flask import make_response


def flatten_json(y):
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + ".")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + ".")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def render_csv(response):
    data = response["data"]
    # Treat single values as a list of one element
    if not isinstance(data, list):
        data = [data]

    # Flatten the list of rows
    rows = []
    fields = set()
    for row in data:
        flattened = flatten_json(row)
        rows.append(flattened)
        fields.update(flattened.keys())

    # Write the rows to CSV
    with StringIO() as out:
        writer = DictWriter(out, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        return make_response(out.getvalue(), 200, {"Content-Type": "text/csv"})
