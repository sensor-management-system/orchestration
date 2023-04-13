# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from ...extensions.idl.models import permission_group
from ...extensions.instances import idl
from ...frj_csv_export.resource import ResourceList
from ..helpers.errors import MethodNotAllowed


class PermissionGroups(ResourceList):
    """
    List the Permission Groups in a json:api style.
    """

    def get(self, *args, **kwargs):
        """
        Retrieve a list of Permission Groups.

        :return: list of Permission Groups.
        """
        data = permission_group.permission_groups_to_list_of_jsonapi_dicts(
            idl.get_permission_groups()
        )
        response = {"data": data}
        response.update({"meta": {"count": len(data)}})
        return response

    def post(self, *args, **kwargs):
        raise MethodNotAllowed("Endpoint is readonly")
