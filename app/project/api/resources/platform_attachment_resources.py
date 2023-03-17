"""Module for the platform attachment list resource."""
import pathlib

from flask import url_for
from flask_rest_jsonapi import JsonApiException, ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...api import minio
from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models.base_model import db
from ..models.platform import Platform
from ..models.platform_attachment import PlatformAttachment
from ..schemas.platform_attachment_schema import PlatformAttachmentSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    delete_attachments_in_minio_by_url,
    query_platform_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
)


class PlatformAttachmentList(ResourceList):
    """
    List resource for platform attachments.

    Provices get and most methods to retrieve a
    collection of platform attachments or to create new ones.
    """

    def query(self, view_kwargs):
        """
        Query the entries from the database.

        Handle also cases to get all the platform attachments
        for a specific platform.
        """
        query_ = get_query_with_permissions_for_related_objects(self.model)
        platform_id = view_kwargs.get("platform_id")

        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Platform: {} not found".format(platform_id),
                )
            else:
                query_ = query_.filter(PlatformAttachment.platform_id == platform_id)
        return query_

    def after_post(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        platform_id = result[0]["data"]["relationships"]["platform"]["data"]["id"]
        attachment_id = result[0]["data"]["id"]
        msg = "create;attachment"
        query_platform_and_set_update_description_text(msg, platform_id)

        data = db.session.query(PlatformAttachment).filter_by(id=attachment_id).first()
        if data and data.url.startswith(minio.download_endpoint(internal=True)):
            data.internal_url = data.url
            last_part_url = pathlib.Path(data.internal_url).name
            data.url = url_for(
                "download.get_platform_attachment_content",
                id=attachment_id,
                filename=last_part_url,
                _external=True,
            )
            db.session.add(data)
            db.session.commit()
            result[0]["data"]["attributes"]["url"] = data.url
            result[0]["data"]["attributes"]["is_upload"] = True

        return result

    def before_create_object(self, data, *args, **kwargs):
        """Set some fields before we save the new entry."""
        add_created_by_id(data)

    schema = PlatformAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformAttachment,
        "methods": {"before_create_object": before_create_object, "query": query},
    }


"""Module for the platform attachment detail resource."""


class PlatformAttachmentDetail(ResourceDetail):
    """
    Resource for platform attachments.

    Provides get, patch & delete methods.
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if PlatformAttachment not found."""
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
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["platform"]["data"]["id"]
        msg = "update;attachment"
        query_platform_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Update the platform update description text."""
        platform_attachment = (
            db.session.query(PlatformAttachment)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if platform_attachment is None:
            raise ObjectNotFound("Object not found!")
        platform = platform_attachment.get_parent()
        msg = "delete;attachment"
        set_update_description_text_and_update_by_user(platform, msg)

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy.

        If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        attachment = (
            db.session.query(PlatformAttachment).filter_by(id=kwargs["id"]).first()
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

    schema = PlatformAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformAttachment,
    }
