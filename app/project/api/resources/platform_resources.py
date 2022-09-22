"""Platform list resource."""

import os

from flask import g, request
from flask_rest_jsonapi import JsonApiException, ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ...api.auth.permission_utils import (
    get_es_query_with_permissions,
    get_query_with_permissions,
    set_default_permission_view_to_internal_if_not_exists_or_all_false,
)
from ...frj_csv_export.resource import ResourceList
from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..helpers.db import save_to_db
from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_updated_by_id
from ..models.base_model import db
from ..models.contact_role import PlatformContactRole
from ..models.platform import Platform
from ..schemas.platform_schema import PlatformSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found, delete_attachments_in_minio_by_url


class PlatformList(ResourceList):
    """
    Resource for the platform list endpoint.

    Supports GET (list) & POST (create) methods.
    """

    def query(self, view_kwargs):
        """
        Filter for what the user is allowed to query.

        :param view_kwargs:
        :return: queryset
        """
        false_values = ["false"]
        # hide archived must be disabled explicitly
        hide_archived = request.args.get("hide_archived") not in false_values
        return get_query_with_permissions(self.model, hide_archived=hide_archived)

    def es_query(self, view_kwargs):
        """
        Return the elasticsearch filter for the query.

        Should return the same set as query, but using
        the elasticsearch fields.
        """
        false_values = ["false"]
        # hide archived must be disabled explicitly
        hide_archived = request.args.get("hide_archived") not in false_values
        return get_es_query_with_permissions(hide_archived=hide_archived)

    def before_create_object(self, data, *args, **kwargs):
        """
        Set the visibility of the object (internal of nothing else is given).

        :param data: data of the request (as dict)
        :param args:
        :param kwargs:
        :return: None
        """
        # Will modify the data inplace.
        set_default_permission_view_to_internal_if_not_exists_or_all_false(data)

    def after_post(self, result):
        """
        Automatically add the created user to object contacts.

        Also add the owner to contact role.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["id"]
        platform = db.session.query(Platform).filter_by(id=result_id).first()
        contact = g.user.contact
        cv_url = os.environ.get("CV_URL")
        role_name = "Owner"
        role_uri = f"{cv_url}/contactroles/4/"
        contact_role = PlatformContactRole(
            contact_id=contact.id,
            platform_id=platform.id,
            role_name=role_name,
            role_uri=role_uri,
        )
        save_to_db(contact_role)

        msg = "create;basic data"
        platform.update_description = msg
        platform.updated_by_id = g.user.id

        save_to_db(platform)

        return result

    schema = PlatformSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Platform,
        "class": EsSqlalchemyDataLayer,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
            "es_query": es_query,
        },
    }


class PlatformDetail(ResourceDetail):
    """
    Detail resource for the platforms.

    Provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a platform.
    """

    def before_get(self, args, kwargs):
        """Return a 404 response if the platform was not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """
        Run logic before the patch.

        In this case we want to make sure that we update the updated_by_id
        with the id of the user that run the request.
        """
        add_updated_by_id(data)

    def after_patch(self, result):
        """
        Run some updates after the patch.

        For example here we can update the update description.
        """
        result_id = result["data"]["id"]
        platform = db.session.query(Platform).filter_by(id=result_id).first()
        msg = "update;basic data"
        platform.update_description = msg
        save_to_db(platform)

        return result

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy.

        If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        platform = db.session.query(Platform).filter_by(id=kwargs["id"]).first()
        if platform is None:
            raise ObjectNotFound({"pointer": ""}, "Object Not Found")
        urls = [a.url for a in platform.platform_attachments]
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError("Deletion failed for the platform.", str(e))

        for url in urls:
            delete_attachments_in_minio_by_url(url)

        final_result = {"meta": {"message": "Object successfully deleted"}}
        return final_result

    schema = PlatformSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Platform,
    }
