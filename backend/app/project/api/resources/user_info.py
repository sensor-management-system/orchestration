# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Resource classes for the user info endpoint."""

from flask import g
from flask_rest_jsonapi import ResourceList

from ..helpers.errors import MethodNotAllowed, UnauthorizedError
from ..models import User
from ..models.base_model import db


class UserInfo(ResourceList):
    """
    JSON API resource to retrieve information about a user.

    It gathers from the local database and the institute decoupling layer.
    User data will be found using the auth mechanism.
    """

    def get(self):
        """
        GET method to retrieve information for a user.

        It is gathered from database and
        Institute decoupling layer (IDL) from user subject.

        :return: Dict with user infos from database + IDL-groups.
        """
        if not g.user:
            raise UnauthorizedError("Authentication required")

        if not g.user.apikey:
            g.user.apikey = User.generate_new_apikey()
            db.session.add(g.user)
            db.session.commit()

        data = {
            "data": {
                "type": "user",
                "id": str(g.user.id),
                "attributes": {
                    "member": [str(m.permission_group.id) for m in g.user.memberships],
                    "active": g.user.active,
                    "is_superuser": g.user.is_superuser,
                    "is_export_control": g.user.is_export_control,
                    "apikey": g.user.apikey,
                    "subject": g.user.subject,
                    "terms_of_use_agreement_date": g.user.terms_of_use_agreement_date,
                },
                "relationships": {
                    "contact": {
                        "data": {"type": "contact", "id": str(g.user.contact_id)}
                    }
                },
            },
        }
        return data

    def post(self, *args, **kwargs):
        """Don't allow post requests."""
        raise MethodNotAllowed("endpoint is readonly")
