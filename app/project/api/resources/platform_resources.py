"""Platform list resource."""

import os

from flask import g, current_app
from flask_rest_jsonapi import JsonApiException, ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from .base_resource import check_if_object_not_found, delete_attachments_in_minio_by_url, add_pid
from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ...api.auth.permission_utils import (
    get_es_query_with_permissions,
    get_query_with_permissions,
    set_default_permission_view_to_internal_if_not_exists_or_all_false,
)
from ..helpers.errors import ConflictError
from ...frj_csv_export.resource import ResourceList
from ..helpers.resource_mixin import add_updated_by_id
from ..models.contact_role import PlatformContactRole
from ..models.platform import Platform
from ..models.base_model import db
from ..schemas.platform_schema import PlatformSchema
from ..token_checker import token_required


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
        return get_query_with_permissions(self.model)

    def es_query(self, view_kwargs):
        """
        Return the elasticsearch filter for the query.

        Should return the same set as query, but using
        the elasticsearch fields.
        """
        return get_es_query_with_permissions()

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
        db.session.add(contact_role)
        db.session.commit()

        if current_app.config["INSTITUTE"] == "ufz":
            sms_frontend_url = current_app.config["SMS_FRONTEND_URL"]
            source_object_url = f"{sms_frontend_url}/platforms/{str(platform.id)}"
            add_pid(platform, source_object_url)

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
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete an Event
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if platform not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.
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

    def before_patch(self, args, kwargs, data):
        """
        Run logic before the patch.

        In this case we want to make sure that we update the updated_by_id
        with the id of the user that run the request.
        """
        add_updated_by_id(data)

    schema = PlatformSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Platform,
    }
