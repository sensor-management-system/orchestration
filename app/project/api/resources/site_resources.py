"""Resource classes for the sites."""
import os

from flask import g, request
from flask_rest_jsonapi import ResourceDetail

from ...frj_csv_export.resource import ResourceList
from ..auth.permission_utils import (
    check_deletion_permission,
    is_superuser,
    is_user_in_a_group,
)
from ..datalayers.esalchemy import (
    AndFilter,
    EsSqlalchemyDataLayer,
    TermEqualsExactStringFilter,
)
from ..helpers.db import save_to_db
from ..helpers.errors import ConflictError, ForbiddenError, UnauthorizedError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Configuration, Site, SiteContactRole
from ..models.base_model import db
from ..schemas.site_schema import SiteSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


class SiteList(ResourceList):
    """List resource for sites (get all, post)."""

    def query(self, view_kwargs):
        """Return the query with some additional filters."""
        query = db.session.query(self.model)
        if not g.user:
            query = query.filter(self.model.is_public)

        false_values = ["false"]
        # hide archived must be disabled explicitly
        hide_archived = request.args.get("hide_archived") not in false_values
        if hide_archived:
            query = query.filter_by(archived=False)
        return query

    def es_query(self, view_kwargs):
        """Create the query for the elasticsearch."""
        and_filters = []
        permission_filter = None
        if not g.user:
            permission_filter = TermEqualsExactStringFilter("is_public", True)
        if permission_filter:
            and_filters.append(permission_filter)

        false_values = ["false"]
        # hide archived must be disabled explicitly
        hide_archived = request.args.get("hide_archived") not in false_values
        if hide_archived:
            and_filters.append(TermEqualsExactStringFilter("archived", False))
        if len(and_filters) == 0:
            return None
        if len(and_filters) == 1:
            return and_filters[0]

        return AndFilter(and_filters)

    def before_create_object(self, data, *args, **kwargs):
        """Do the pre-processing before we save our data."""
        if not any([data.get("is_public"), data.get("is_internal")]):
            data["is_internal"] = True
            data["is_public"] = False
        add_created_by_id(data)

    def after_post(self, result):
        """Add some more data to the new site."""
        result_id = result[0]["data"]["id"]
        site = db.session.query(Site).filter_by(id=result_id).first()
        contact = g.user.contact
        cv_url = os.environ.get("CV_URL")
        role_name = "Owner"
        role_uri = f"{cv_url}/contactroles/4/"
        contact_role = SiteContactRole(
            contact_id=contact.id,
            site_id=site.id,
            role_name=role_name,
            role_uri=role_uri,
        )
        db.session.add(contact_role)

        msg = "create;basic data"
        site.update_description = msg
        site.updated_by = g.user

        save_to_db(site)

        return result

    schema = SiteSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Site,
        "methods": {
            "query": query,
            "es_query": es_query,
            "before_create_object": before_create_object,
        },
        "class": EsSqlalchemyDataLayer,
    }


class SiteDetail(ResourceDetail):
    """Detail resource for sites (get one, patch, delete)."""

    def before_get(self, args, kwargs):
        """Prevent not registered users form viewing internal configs."""
        check_if_object_not_found(self._data_layer.model, kwargs)
        site = db.session.query(Site).filter_by(id=kwargs["id"]).first()
        if site:
            if site.is_internal:
                if not g.user:
                    raise UnauthorizedError("Authentication required.")

    def before_patch(self, args, kwargs, data):
        """Run some checks before patching."""
        site = db.session.query(Site).filter_by(id=data["id"]).one_or_none()
        if site and site.archived:
            raise ConflictError("It is not allowed to edit archived sites.")
        if not is_superuser():
            group_ids = site.group_ids
            if group_ids:
                if not is_user_in_a_group(group_ids):
                    raise ForbiddenError(
                        "User is not part of any group to edit this object."
                    )
        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some updates after the successful patch."""
        result_id = result["data"]["id"]
        site = db.session.query(Site).filter_by(id=result_id).first()
        msg = "update;basic data"
        site.update_description = msg
        save_to_db(site)

        return result

    def before_delete(self, args, kwargs):
        """Run some checks before deleting."""
        check_deletion_permission(kwargs, Site)
        associated_configuration = (
            db.session.query(Configuration).filter_by(site_id=kwargs["id"]).first()
        )
        if associated_configuration:
            raise ConflictError("There are configurations associated to this site.")

    schema = SiteSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Site,
    }
