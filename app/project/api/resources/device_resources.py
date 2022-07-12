"""Device list resource."""

import os

from flask import g, current_app, request
from flask_rest_jsonapi import JsonApiException, ResourceDetail

from ...frj_csv_export.resource import ResourceList
from .base_resource import (
    check_if_object_not_found,
    delete_attachments_in_minio_by_url,
    add_pid,
)
from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..helpers.db import save_to_db
from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_updated_by_id
from ..models.base_model import db
from ..models.contact_role import DeviceContactRole
from ..models.device import Device
from ..schemas.device_schema import DeviceSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found, delete_attachments_in_minio_by_url

from ...api.auth.permission_utils import (
    get_es_query_with_permissions,
    get_query_with_permissions,
    set_default_permission_view_to_internal_if_not_exists_or_all_false,
)
from ...extensions.instances import pid
from ...frj_csv_export.resource import ResourceList


class DeviceList(ResourceList):
    """
    Resource for the device list endpoint.

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
        device = db.session.query(Device).filter_by(id=result_id).first()
        contact = g.user.contact
        cv_url = os.environ.get("CV_URL")
        role_name = "Owner"
        role_uri = f"{cv_url}/contactroles/4/"
        contact_role = DeviceContactRole(
            contact_id=contact.id,
            device_id=device.id,
            role_name=role_name,
            role_uri=role_uri,
        )
        save_to_db(contact_role)

        msg = "create;basic data"
        device.update_description = msg
        device.updated_by_id = g.user.id

        save_to_db(device)

        #if current_app.config["INSTITUTE"] == "ufz":
        #    sms_frontend_url = current_app.config["SMS_FRONTEND_URL"]
        #    source_object_url = f"{sms_frontend_url}/devices/{str(device.id)}"
        #    add_pid(device, source_object_url)

        return result

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
        "class": EsSqlalchemyDataLayer,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
            "es_query": es_query,
        },
    }


class DeviceDetail(ResourceDetail):
    """
    Detail resource class for devices.

    Provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device.
    """

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.

        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        device = check_if_object_not_found(Device, kwargs)

        if current_app.config["INSTITUTE"] == "ufz":
            pid_to_delete = device.persistent_identifier
            if pid_to_delete and pid.get(pid_to_delete).status_code == 200:
                pid.delete(pid_to_delete)

        urls = [a.url for a in device.device_attachments]
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError("Deletion failed for the device.", str(e))

        for url in urls:
            delete_attachments_in_minio_by_url(url)

        if current_app.config["INSTITUTE"] == "ufz":
            pid_to_delete = device.persistent_identifier
            pid.delete_a_pid(pid_to_delete)

        final_result = {"meta": {"message": "Object successfully deleted"}}
        return final_result

    def before_patch(self, args, kwargs, data):
        """
        Run logic before the patch.

        In this case we want to make sure that we update the updated_by_id
        with the id of the user that run the request.
        In Flask those data should be stored in the `g` object.
        """
        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some update logic after the change by the patch request."""
        result_id = result["data"]["id"]
        device = db.session.query(Device).filter_by(id=result_id).first()
        msg = "update;basic data"
        device.update_description = msg

        save_to_db(device)

        return result

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
    }
