# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Utility functions to work with dicts."""


def dict_from_kv_list(kv_list):
    """Transform a list with first the key and then the value item to a dict.

    >>> dict_from_kv_list("a", "b", "c", "d")
    {"a": "b", "c": "d"}
    """
    result = {}
    for key, value in zip(kv_list[::2], kv_list[1::2]):
        result[key] = value
    return result
