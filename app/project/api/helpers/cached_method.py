# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Some logic for cache method decorator."""
import functools

import cachetools


def cached_method(
    cache, skip_argument=None, key=cachetools.keys.methodkey, *c_args, **c_kwargs
):
    """
    Decorate a method so that a cache of an class instance can be used.

    This is an extention of the chachedmethod decorator of the cachetools
    package.
    What we add here is the option to run an request & invalidate the
    existing cached result.

    So we can write something like:

    class F:
        def __init__(self):
            self.cache = TTLCache(maxsize=1000, ttl=1000)

        @cachedmethod(operators.attrgetter("cache), skip_arguments={"fresh": True})
        def f(self, x):
            return x + 3

    We can can use it like the usual cachedmethod:

    f_inst = F()
    f_inst.f(3)
    f_inst.f(3) # Returns the cached result

    But we can also force it to return a result without cache lookup with:

    f_inst.f(3, fresh=True)
    """
    if skip_argument is None:
        skip_argument = {}

    def inner(f):
        cached = cachetools.cachedmethod(cache, *c_args, key=key, **c_kwargs)(f)

        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            if skip_argument.keys():
                skip_argument_key = next(iter(skip_argument))
                skip_argument_value = skip_argument[skip_argument_key]

                filtered_kwargs = {
                    k: v for k, v in kwargs.items() if k != skip_argument_key
                }
                if skip_argument_key in kwargs.keys():
                    if kwargs[skip_argument_key] == skip_argument_value:
                        cache_key = key(self, *args, **filtered_kwargs)
                        c = cache(self)
                        if cache_key in c.keys():
                            del c[cache_key]
            else:
                filtered_kwargs = kwargs
            result = cached(self, *args, **filtered_kwargs)
            return result

        return wrapper

    return inner

    return inner
