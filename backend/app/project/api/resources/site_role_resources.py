# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resources for site contact roles."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.exc import NoResultFound

from ..models import Site
from ..models.base_model import db
from ..models.contact_role import SiteContactRole
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.role import SiteRoleSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_site_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class SiteRoleList(ResourceList):
    """
    List resource for site contact roles.

    Provides get and post methods to retrieve
    a collection of site contact roles or create one.
    """

    def query(self, view_kwargs):
        """Query the entries from the database."""
        query_ = filter_visible(self.session.query(self.model))
        site_id = view_kwargs.get("site_id")

        if site_id is not None:
            try:
                self.session.query(Site).filter_by(id=site_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"},
                    "Site: {} not found".format(site_id),
                )
            query_ = query_.filter(SiteContactRole.site_id == site_id)
        return query_

    def after_post(self, result):
        """Run some hooks after the post."""
        result_id = result[0]["data"]["relationships"]["site"]["data"]["id"]
        msg = "create;contact"
        query_site_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = SiteRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": SiteContactRole,
        "methods": {"query": query},
    }
    permission_classes = [DelegateToCanFunctions]


class SiteRoleDetail(ResourceDetail):
    """
    Detail resource for site contact roles.

    Provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a site contact role.
    """

    def before_get(self, args, kwargs):
        """
        Return 404 Responses if role not found.

        Also check if we are allowed to see the entry.
        """
        check_if_object_not_found(self._data_layer.model, kwargs)

    def after_patch(self, result):
        """Rune some hooks after the patch of the contact role."""
        site_id = result["data"]["relationships"]["site"]["data"]["id"]
        msg = "update;contact"
        query_site_set_update_description_and_update_pidinst(msg, site_id)
        return result

    def before_delete(self, args, kwargs):
        """Check permissions to delete."""
        contact_role = (
            db.session.query(SiteContactRole).filter_by(id=kwargs["id"]).one_or_none()
        )
        if contact_role is None:
            raise ObjectNotFound("Object not found!")
        self.tasks_after_delete = []
        site = contact_role.get_parent()
        msg = "delete;contact"

        def run_updates():
            """Set the update description & update external metadata for pidinst."""
            set_update_description_text_user_and_pidinst(site, msg)

        self.tasks_after_delete.append(run_updates)

    def after_delete(self, *args, **kwargs):
        """Run some hooks after deleting."""
        for task in self.tasks_after_delete:
            task()
        return super().after_delete(*args, **kwargs)

    schema = SiteRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": SiteContactRole,
    }
    permission_classes = [DelegateToCanFunctions]
