# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Permission manager function to handle multiple views."""

from flask import g

from ..helpers.errors import ForbiddenError, UnauthorizedError


def permission_manager(view, view_args, view_kwargs, *args, **kwargs):
    """
    Check permissions for various views.

    Register here the permission class checks that each resource class
    defines.

    :param callable view: the view
    :param list view_args: view args
    :param dict view_kwargs: view kwargs
    :param list args: decorator args
    :param dict kwargs: decorator kwargs
    """
    # The first entry in the view args contains the resource instance.
    if view_args:
        resource = view_args[0]
        if hasattr(resource, "permission_classes"):
            for p in resource.permission_classes:
                p_inst = p()
                # Currently I throw the exception if one of the options
                # isn't valid. Maybe it makes sense to change that.
                if not p_inst.has_permission(
                    view, view_args, view_kwargs, *args, **kwargs
                ):
                    # Now it is the question, which exception to throw.
                    # If we don't have a user, it could help to return 401.
                    # That way the user can try to login & try it again.
                    if not g.user:
                        raise UnauthorizedError("Authentication required")
                    # Otherwise, we just throw an 403.
                    raise ForbiddenError("Request not allowed")
