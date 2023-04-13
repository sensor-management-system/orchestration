# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Module for the configuration attachments list resource."""
import pathlib

from flask import url_for
from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import JsonApiException, ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...api import minio
from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Configuration, ConfigurationAttachment
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.configuration_attachment_schema import ConfigurationAttachmentSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    delete_attachments_in_minio_by_url,
    query_configuration_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
)


class ConfigurationAttachmentList(ResourceList):
    """List resource for configuration attachments."""

    def query(self, view_kwargs):
        """Query the entries from the database."""
        query_ = filter_visible(self.session.query(self.model))
        configuration_id = view_kwargs.get("configuration_id")

        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Configuration: {} not found".format(configuration_id),
                )
            else:
                query_ = query_.filter(
                    ConfigurationAttachment.configuration_id == configuration_id
                )
        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Set some fields before we save the new entry."""
        add_created_by_id(data)

    def after_post(self, result):
        """
        Add update description to related configuraiton.

        :param result:
        :return:
        """
        configuration_id = result[0]["data"]["relationships"]["configuration"]["data"][
            "id"
        ]
        attachment_id = result[0]["data"]["id"]
        msg = "create;attachment"
        query_configuration_and_set_update_description_text(msg, configuration_id)
        data = (
            db.session.query(ConfigurationAttachment)
            .filter_by(id=attachment_id)
            .first()
        )
        if data and data.url.startswith(minio.download_endpoint(internal=True)):
            data.internal_url = data.url
            last_part_url = pathlib.Path(data.internal_url).name
            data.url = url_for(
                "download.get_configuration_attachment_content",
                id=attachment_id,
                filename=last_part_url,
                _external=True,
            )
            db.session.add(data)
            db.session.commit()
            result[0]["data"]["attributes"]["url"] = data.url
            result[0]["data"]["attributes"]["is_upload"] = True

        return result

    schema = ConfigurationAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationAttachment,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class ConfigurationAttachmentDetail(ResourceDetail):
    """Resource for ConfigurationAttachments."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if ConfigurationAttachment not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data=None):
        """Add handling for uploads from our file storage."""
        attachment = (
            db.session.query(self._data_layer.model).filter_by(id=kwargs["id"]).first()
        )
        if attachment and attachment.is_upload:
            if data["url"] and data["url"] != attachment.url:
                raise ConflictError("It is not allowed to change the url of uploads")
        add_updated_by_id(data)

    def after_patch(self, result):
        """
        Add update description to related configuration.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "update;attachment"
        query_configuration_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Update the configurations update description."""
        configuration_attachment = (
            db.session.query(ConfigurationAttachment)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if configuration_attachment is None:
            raise ObjectNotFound("Object not found!")
        configuration = configuration_attachment.get_parent()
        msg = "delete;attachment"
        set_update_description_text_and_update_by_user(configuration, msg)

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy.

        If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        attachment = (
            db.session.query(ConfigurationAttachment).filter_by(id=kwargs["id"]).first()
        )
        if attachment is None:
            raise ObjectNotFound({"pointer": ""}, "Object Not Found")
        internal_url = attachment.internal_url
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError(
                "Deletion failed as the attachment is still in use.", str(e)
            )

        if internal_url:
            delete_attachments_in_minio_by_url(internal_url)
        final_result = {"meta": {"message": "Object successfully deleted"}}

        return final_result

    schema = ConfigurationAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationAttachment,
    }
    permission_classes = [DelegateToCanFunctions]
