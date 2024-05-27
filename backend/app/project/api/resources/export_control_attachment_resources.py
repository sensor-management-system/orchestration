# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2


"""Module for the export control attachment list resource."""

import pathlib

from flask import url_for
from flask_rest_jsonapi import JsonApiException, ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...api import minio
from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import (
    Device,
    ExportControl,
    ExportControlAttachment,
    ManufacturerModel,
    Platform,
)
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.export_control_attachment_schema import ExportControlAttachmentSchema
from .base_resource import check_if_object_not_found, delete_attachments_in_minio_by_url


class ExportControlAttachmentList(ResourceList):
    """List endpoint resource for the export control attachments."""

    def query(self, view_kwargs):
        """Filter the entities."""
        query_ = filter_visible(self.session.query(self.model))

        manufacturer_model_id = view_kwargs.get("manufacturer_model_id")

        if manufacturer_model_id is not None:
            try:
                self.session.query(ManufacturerModel).filter_by(
                    id=manufacturer_model_id
                ).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "ManufacturerModel: {} not found".format(manufacturer_model_id),
                )
            else:
                query_ = query_.filter(
                    ExportControlAttachment.manufacturer_model_id
                    == manufacturer_model_id
                )
        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Add the created by information."""
        add_created_by_id(data)

    def after_post(self, result):
        """Eventuelly change the url."""
        attachment_id = result[0]["data"]["id"]

        data = (
            db.session.query(ExportControlAttachment)
            .filter_by(id=attachment_id)
            .first()
        )
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
                "download.get_export_control_attachment_content",
                id=attachment_id,
                filename=last_part_url,
                _external=True,
            )
            db.session.add(data)
            db.session.commit()
            result[0]["data"]["attributes"]["url"] = data.url
            result[0]["data"]["attributes"]["is_upload"] = True

        return result

    schema = ExportControlAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": ExportControlAttachment,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class ExportControlAttachmentDetail(ResourceDetail):
    """Detail endpoint resource for the export control attachments."""

    def before_get(self, args, kwargs):
        """Run some tests before the get method."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Add the updated by field."""
        attachment = (
            db.session.query(self._data_layer.model).filter_by(id=kwargs["id"]).first()
        )
        if attachment and attachment.is_upload:
            if data["url"] and data["url"] != attachment.url:
                raise ConflictError("It is not allowed to change the url of uploads")
        if data.get("manufacturer_model"):
            if attachment.manufacturer_model_id != data["manufacturer_model"]:
                raise ConflictError(
                    "Changing the manufacturer model relationship is not allowed"
                )
        add_updated_by_id(data)

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy.

        If this could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        attachment = (
            db.session.query(ExportControlAttachment).filter_by(id=kwargs["id"]).first()
        )
        if attachment is None:
            raise ObjectNotFound({"pointer": ""}, "Object Not Found")
        manufacturer_model = attachment.manufacturer_model
        internal_url = attachment.internal_url
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError(
                "Deletion failed as the attachment is still in use.", str(e)
            )

        if internal_url:
            delete_attachments_in_minio_by_url(internal_url)

        can_delete_manfuacturer_model_too = True

        if (
            manufacturer_model.external_system_name
            or manufacturer_model.external_system_url
        ):
            can_delete_manfuacturer_model_too = False
        elif (
            self._data_layer.session.query(Device)
            .filter_by(
                manufacturer_name=manufacturer_model.manufacturer_name,
                model=manufacturer_model.model,
            )
            .first()
        ):
            can_delete_manfuacturer_model_too = False
        elif (
            self._data_layer.session.query(Platform)
            .filter_by(
                manufacturer_name=manufacturer_model.manufacturer_name,
                model=manufacturer_model.model,
            )
            .first()
        ):
            can_delete_manfuacturer_model_too = False
        elif (
            self._data_layer.session.query(ExportControl)
            .filter_by(manufacturer_model=manufacturer_model)
            .first()
        ):
            can_delete_manfuacturer_model_too = False

        if can_delete_manfuacturer_model_too:
            self._data_layer.session.delete(manufacturer_model)
            self._data_layer.session.commit()
        final_result = {"meta": {"message": "Object successfully deleted"}}

        return final_result

    schema = ExportControlAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": ExportControlAttachment,
    }
    permission_classes = [DelegateToCanFunctions]
