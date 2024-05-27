# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Mixin for the csv export."""

import re
import pandas as pd
from cherrypicker import CherryPicker
from flask import request
from flask_rest_jsonapi.querystring import QueryStringManager as QSManager
from werkzeug.wrappers import Response


def render_csv(response):
    """Transform a pandas data frame to csv."""
    return Response(
        response.to_csv(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=export.csv"},
    )


def transform_to_series(objects, schema, replace_newlines_with_spaces=False):
    """
    Convert list of dictionaries to a pandas DataFrame.

    :param objects: a list of the objects
    :param schema: MarshmallowSchema for the object
    :return: dataframe
    """
    # CherryPicker for restructuring the data into flat tables
    # use the to_search_entry() to get the mode as a dict
    list_of_flat_dicts = []
    for obj in objects:
        picker = CherryPicker(schema().nested_dict_serializer(obj))
        flat_dict = picker.flatten().get()
        if replace_newlines_with_spaces:
            for key, value in flat_dict.items():
                if isinstance(value, str):
                    clean_value = re.sub("\n+", " ", value)
                    flat_dict[key] = clean_value
        list_of_flat_dicts.append(flat_dict)

    # json_normalize() works with lists of dictionaries (records) to convert the list
    # to a pandas DataFrame, and in addition can also handle nested dictionaries.
    df = pd.json_normalize(list_of_flat_dicts)
    return df


class CsvListMixin:
    """Mixin for list resources so that we can export data as csv."""

    def get(self, *args, **kwargs):
        """Return the GET response a resource - possibly as csv."""
        if "HTTP_ACCEPT" in request.headers.environ:
            http_accept = request.headers.environ["HTTP_ACCEPT"]
            if http_accept == "text/csv":
                return self.transform_to_csv(*args, **kwargs)
        return super().get(*args, **kwargs)

    def transform_to_csv(self, *args, **kwargs):
        """Return the response as CSV."""
        self.before_get(args, kwargs)
        qs = QSManager(request.args, self.schema)
        parent_filter = self._get_parent_filter(request.url, kwargs)
        objects_count, objects = self.get_collection(qs, kwargs, filters=parent_filter)
        return render_csv(
            transform_to_series(objects, self.schema, replace_newlines_with_spaces=True)
        )
