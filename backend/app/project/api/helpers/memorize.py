# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Decorator to run functions or methods only once."""

import functools
import pickle


def memorize(f):
    """Memorize a function so that we run that only one single time."""
    results = {}

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        key = pickle.dumps((args, kwargs))
        if key in results.keys():
            return results[key]

        result = f(*args, **kwargs)
        results[key] = result
        return result

    return wrapper
