# SPDX-FileCopyrightText: 2026
# - Nils Brinckmann <nils.brinckmann@gfz.de>
# - GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Resource classes for the organizations."""

from flask_rest_jsonapi import ResourceDetail, ResourceList

from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..helpers.errors import ConflictError
from ..models import Contact, Organization
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible, filter_visible_es
from ..schemas.organization_schema import OrganizationSchema
from .base_resource import check_if_object_not_found


class OrganizationList(ResourceList):
    """List resource for the organization (GET, POST)."""

    def query(self, view_kwargs):
        """Return the query for the search."""
        query = filter_visible(self.session.query(self.model))
        return query

    def es_query(self, view_kwargs):
        """Return the filter for the elasticsearch query."""
        return filter_visible_es(self.model)

    schema = OrganizationSchema

    data_layer = {
        "session": db.session,
        "model": Organization,
        "class": EsSqlalchemyDataLayer,
        "methods": {"query": query, "es_query": es_query},
    }
    permission_classes = [DelegateToCanFunctions]


class OrganizationDetail(ResourceDetail):
    """Detail resource for the organization (GET, PATCH, DELETE)."""

    def before_get(self, args, kwargs):
        """Run some tests before the get method."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Ensure that the contacts keep updated information."""
        current_id = kwargs["id"]
        current_organization = (
            db.session.query(Organization).filter_by(id=current_id).first()
        )
        new_name = data.get("name")
        if new_name and current_organization and new_name != current_organization.name:
            current_contacts_with_this_organization = db.session.query(
                Contact
            ).filter_by(organization=current_organization.name)
            for contact in current_contacts_with_this_organization:
                contact.organization = new_name
                db.session.add(contact)

    def before_delete(self, args, kwargs):
        """Ensure we don't delete organizations with associated contacts."""
        organization = check_if_object_not_found(self._data_layer.model, kwargs)

        still_assigned_contact = (
            db.session.query(Contact).filter_by(organization=organization.name).first()
        )
        if still_assigned_contact:
            raise ConflictError(
                "Organization has still associated contacts and can't be deleted"
            )

    schema = OrganizationSchema
    data_layer = {
        "session": db.session,
        "model": Organization,
    }
    permission_classes = [DelegateToCanFunctions]
