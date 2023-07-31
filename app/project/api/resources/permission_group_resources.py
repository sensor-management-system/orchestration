# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resource class for the list of permission groups."""

from flask import request
from flask_rest_jsonapi import ResourceList

from ...extensions.idl.models import permission_group
from ...extensions.instances import idl
from ..helpers.errors import MethodNotAllowed


class PermissionGroups(ResourceList):
    """List the Permission Groups in a json:api style."""

    def get(self, *args, **kwargs):
        """
        Retrieve a list of Permission Groups.

        :return: list of Permission Groups.
        """
        skip_cache_arguments = {}
        # type is a function where we put the string value in.
        # A little bit annoying...
        if request.args.get(
            "skip_cache", default=False, type=lambda x: x.lower() == "true"
        ):
            skip_cache_arguments["skip_cache"] = True

        data = permission_group.permission_groups_to_list_of_jsonapi_dicts(
            idl.get_permission_groups(**skip_cache_arguments)
        )
        response = {"data": data}
        response.update({"meta": {"count": len(data)}})
        return response

    def post(self, *args, **kwargs):
        """Don't allow post requests."""
        raise MethodNotAllowed("Endpoint is readonly")
