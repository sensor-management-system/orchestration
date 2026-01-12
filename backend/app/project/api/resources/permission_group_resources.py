# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Resource class for the list of permission groups."""

from flask_rest_jsonapi import ResourceList

from ..helpers.errors import MethodNotAllowed
from ..models import PermissionGroup
from ..models.base_model import db


class PermissionGroups(ResourceList):
    """List the Permission Groups in a json:api style."""

    def get(self, *args, **kwargs):
        """
        Retrieve a list of Permission Groups.

        :return: list of Permission Groups.
        """
        data = []

        for pm in db.session.query(PermissionGroup).all():
            data.append(
                {
                    "id": str(pm.id),
                    "type": "permission_group",
                    "attributes": {
                        "name": pm.name,
                        "entitlement": pm.entitlement,
                        "description": "",
                    },
                }
            )

        response = {"data": data}
        response.update({"meta": {"count": len(data)}})
        return response

    def post(self, *args, **kwargs):
        """Don't allow post requests."""
        raise MethodNotAllowed("Endpoint is readonly")
