"""Configuration list resource."""

import os

from flask import g
from flask_rest_jsonapi import JsonApiException, ResourceDetail
from sqlalchemy import or_

from .base_resource import check_if_object_not_found, delete_attachments_in_minio_by_url
from ..auth.permission_utils import (
    cfg_permission_group_defined,
    check_deletion_permission,
    is_superuser,
    is_user_in_a_group,
)
from ..datalayers.esalchemy import (
    EsSqlalchemyDataLayer,
    OrFilter,
    TermEqualsExactStringFilter,
)
from ..helpers.db import save_to_db
from ..helpers.errors import ConflictError, ForbiddenError, UnauthorizedError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.contact_role import ConfigurationContactRole
from ..schemas.configuration_schema import ConfigurationSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class ConfigurationList(ResourceList):
    """
    Resource for the device list endpoint.

    Supports GET (list) & POST (create) methods.
    """

    def query(self, view_kwargs):
        """
        Filter for what the user is allowed to query.

        :param view_kwargs:
        :return: queryset or es filter
        """
        query = db.session.query(self.model)
        if g.user is None:
            query = query.filter_by(is_public=True)
        else:
            if not g.user.is_superuser:
                query = query.filter(or_(self.model.is_public, self.model.is_internal,))
        return query

    def es_query(self, view_kwargs):
        """
        Return the elasticsearch filter for the query.

        Should return the same set as query, but using
        the elasticsearch fields.
        """
        if g.user is None:
            return TermEqualsExactStringFilter("is_public", True)
        if not g.user.is_superuser:
            return OrFilter(
                [
                    TermEqualsExactStringFilter("is_public", True),
                    TermEqualsExactStringFilter("is_internal", True),
                ]
            )
        return None

    def before_create_object(self, data, *args, **kwargs):
        """
        Set the visibility of the object (internal of nothing else is given).

        :param data: data of the request (as dict)
        :param args:
        :param kwargs:
        :return: None
        """
        # Will modify the data inplace.
        if not any([data.get("is_public"), data.get("is_internal")]):
            data["is_internal"] = True
            data["is_public"] = False
        add_created_by_id(data)

    def after_post(self, result):
        """
        Automatically add the created user to object contacts.

        Also add the owner to contact role.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["id"]
        configuration = db.session.query(Configuration).filter_by(id=result_id).first()
        contact = g.user.contact
        cv_url = os.environ.get("CV_URL")
        role_name = "Owner"
        role_uri = f"{cv_url}/contactroles/4/"
        contact_role = ConfigurationContactRole(
            contact_id=contact.id,
            configuration_id=configuration.id,
            role_name=role_name,
            role_uri=role_uri,
        )
        db.session.add(contact_role)

        msg = "create;basic data"
        configuration.update_description = msg
        configuration.updated_by_id = g.user.id

        save_to_db(configuration)

        return result

    schema = ConfigurationSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Configuration,
        "class": EsSqlalchemyDataLayer,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
            "es_query": es_query,
        },
    }


class ConfigurationDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    def before_get(self, args, kwargs):
        """Prevent not registered users form viewing internal configs."""
        check_if_object_not_found(self._data_layer.model, kwargs)
        config = db.session.query(Configuration).filter_by(id=kwargs["id"]).first()
        if config:
            if config.is_internal:
                if not g.user:
                    raise UnauthorizedError("Authentication required.")

    def before_patch(self, args, kwargs, data):
        """check if a user has the permission to change this configuration"""
        if not is_superuser():
            configuration = (
                db.session.query(Configuration).filter_by(id=data["id"]).one_or_none()
            )
            group_id = configuration.cfg_permission_group
            if cfg_permission_group_defined(group_id):
                if not is_user_in_a_group([group_id]):
                    raise ForbiddenError(
                        "User is not part of any group to edit this object."
                    )
        add_updated_by_id(data)

    def after_patch(self, result):
        result_id = result["data"]["id"]
        configuration = db.session.query(Configuration).filter_by(id=result_id).first()
        msg = "update;basic data"
        configuration.update_description = msg

        save_to_db(configuration)
        return result

    def before_delete(self, args, kwargs):
        """Checks for permission"""
        check_deletion_permission(kwargs, Configuration)

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        configuration = check_if_object_not_found(Configuration, kwargs)
        urls = [a.url for a in configuration.configuration_attachments]
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError("Deletion failed for the configuration.", str(e))

        for url in urls:
            delete_attachments_in_minio_by_url(url)

        final_result = {"meta": {"message": "Object successfully deleted"}}
        return final_result

    schema = ConfigurationSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Configuration,
    }
