# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Some logic for generic functions with custom dispatcher logic."""
import functools


def custom_dispatch(dispatch):
    """Decorate so we can use several implementations selected by the dispatcher."""
    registry = {}

    default_function = None

    @functools.wraps(dispatch)
    def wrapper(*args, **kwargs):
        dispatch_result = dispatch(*args, **kwargs)
        func = registry.get(dispatch_result, default_function)
        if not func:
            raise NotImplementedError()
        return func(*args, **kwargs)

    def default(f):
        nonlocal default_function
        default_function = f
        return wrapper

    def register(dispatch_result):
        def register_wrapper(f):
            registry[dispatch_result] = f
            return wrapper

        return register_wrapper

    def register_many(*dispatch_results):
        def register_many_wrapper(f):
            for dispatch_result in dispatch_results:
                registry[dispatch_result] = f
            return wrapper

        return register_many_wrapper

    def register_same(dispatch_result, handler):
        registry[dispatch_result] = registry.get(handler, default_function)
        return wrapper

    def find_for(dispatch_result):
        func = registry.get(dispatch_result, default_function)
        if not func:
            raise NotImplementedError()
        return func

    def delegate(dispatch_result, *args, **kwargs):
        return find_for(dispatch_result)(*args, **kwargs)

    wrapper.default = default
    wrapper.delegate = delegate
    wrapper.dispatch = dispatch
    wrapper.find_for = find_for
    wrapper.register = register
    wrapper.register_many = register_many
    wrapper.register_same = register_same
    return wrapper
