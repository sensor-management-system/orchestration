"""Resource classes for the sites."""
import os

from flask import g, request
from flask_rest_jsonapi import ResourceDetail

from ...frj_csv_export.resource import ResourceList
from ..datalayers.esalchemy import (
    AndFilter,
    EsSqlalchemyDataLayer,
    TermEqualsExactStringFilter,
)
from ..helpers.db import save_to_db
from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Configuration, Site, SiteContactRole
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible, filter_visible_es
from ..schemas.site_schema import SiteSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


class SiteList(ResourceList):
    """List resource for sites (get all, post)."""

    def query(self, view_kwargs):
        """Return the query with some additional filters."""
        query = filter_visible(self.session.query(self.model))

        false_values = ["false"]
        # hide archived must be disabled explicitly
        hide_archived = request.args.get("hide_archived") not in false_values
        if hide_archived:
            query = query.filter_by(archived=False)
        return query

    def es_query(self, view_kwargs):
        """Create the query for the elasticsearch."""
        and_filters = [filter_visible_es(self.model)]

        false_values = ["false"]
        # hide archived must be disabled explicitly
        hide_archived = request.args.get("hide_archived") not in false_values
        if hide_archived:
            and_filters.append(TermEqualsExactStringFilter("archived", False))
        return AndFilter.combine_optionals(and_filters)

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
    permission_classes = [DelegateToCanFunctions]


class SiteDetail(ResourceDetail):
    """Detail resource for sites (get one, patch, delete)."""

    def before_patch(self, args, kwargs, data):
        """Run some checks before patching."""
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
        associated_configuration = (
            db.session.query(Configuration).filter_by(site_id=kwargs["id"]).first()
        )
        if associated_configuration:
            raise ConflictError("There are configurations associated to this site.")

    def before_get(self, args, kwargs):
        """Run some tests before the get method."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = SiteSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Site,
    }
    permission_classes = [DelegateToCanFunctions]
