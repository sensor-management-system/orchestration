# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Module for the device attachment list resource."""
import pathlib

from flask import url_for
from flask_rest_jsonapi import JsonApiException, ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...api import minio
from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models.base_model import db
from ..models.device import Device
from ..models.device_attachment import DeviceAttachment
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.device_attachment_schema import DeviceAttachmentSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    delete_attachments_in_minio_by_url,
    query_device_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class DeviceAttachmentList(ResourceList):
    """
    List resource for device attachments.

    Provides get and most methods to retrieve a
    collection of device attachments or to create new ones.
    """

    def query(self, view_kwargs):
        """
        Query the entries from the database.

        Handle also additional logic to query the device
        attachments for a specific device.
        """
        query_ = filter_visible(self.session.query(self.model))
        device_id = view_kwargs.get("device_id")

        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(DeviceAttachment.device_id == device_id)
        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Set some fields before we save the new entry."""
        add_created_by_id(data)

    def after_post(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        device_id = result[0]["data"]["relationships"]["device"]["data"]["id"]
        attachment_id = result[0]["data"]["id"]
        msg = "create;attachment"
        query_device_set_update_description_and_update_pidinst(msg, device_id)

        data = db.session.query(DeviceAttachment).filter_by(id=attachment_id).first()
        if data and data.url.startswith(minio.download_endpoint(internal=True)):
            # If we uploaded with an internal filestorage url, we want
            # to replace it, so that the user can query the file only
            # via the backend (and with the permission checks that run).
            # This way we can make sure that only those users that are
            # allowed to see the content can actually see them.
            #
            # We do that by storing it as an internal url and give
            # back a link that the user can use to retrieve it.
            data.internal_url = data.url
            last_part_url = pathlib.Path(data.internal_url).name
            data.url = url_for(
                "download.get_device_attachment_content",
                id=attachment_id,
                filename=last_part_url,
                _external=True,
            )
            db.session.add(data)
            db.session.commit()
            result[0]["data"]["attributes"]["url"] = data.url
            result[0]["data"]["attributes"]["is_upload"] = True

        return result

    schema = DeviceAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceAttachment,
        "methods": {"before_create_object": before_create_object, "query": query},
    }
    permission_classes = [DelegateToCanFunctions]


class DeviceAttachmentDetail(ResourceDetail):
    """
    Resource for device attachments.

    Provides get, patch & delete methods.
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceAttachment not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some checks before updating the data."""
        attachment = (
            db.session.query(self._data_layer.model).filter_by(id=kwargs["id"]).first()
        )
        if attachment and attachment.is_upload:
            if data["url"] and data["url"] != attachment.url:
                raise ConflictError("It is not allowed to change the url of uploads")
        add_updated_by_id(data)

    def after_patch(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["device"]["data"]["id"]
        msg = "update;attachment"
        query_device_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy.

        If this could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        attachment = (
            db.session.query(DeviceAttachment).filter_by(id=kwargs["id"]).first()
        )
        if attachment is None:
            raise ObjectNotFound({"pointer": ""}, "Object Not Found")
        device = attachment.get_parent()
        msg = "delete;attachment"
        internal_url = attachment.internal_url
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError(
                "Deletion failed as the attachment is still in use.", str(e)
            )

        if internal_url:
            delete_attachments_in_minio_by_url(internal_url)
        set_update_description_text_user_and_pidinst(device, msg)
        final_result = {"meta": {"message": "Object successfully deleted"}}

        return final_result

    schema = DeviceAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceAttachment,
    }
    permission_classes = [DelegateToCanFunctions]
