"""Module for the platform attachment list resource."""
from flask_rest_jsonapi import JsonApiException, ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import \
    get_query_with_permissions_for_related_objects
from ..helpers.errors import ConflictError
from ..models.base_model import db
from ..models.platform import Platform
from ..models.platform_attachment import PlatformAttachment
from ..schemas.platform_attachment_schema import PlatformAttachmentSchema
from ..token_checker import token_required
from .base_resource import (check_if_object_not_found,
                            delete_attachments_in_minio_by_url,
                            query_platform_and_set_update_description_text,
                            set_update_description_text_and_update_by_user)


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
                    {"parameter": "id",}, "Platform: {} not found".format(platform_id),
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
        result_id = result[0]["data"]["relationships"]["platform"]["data"]["id"]
        msg = "create;attachment"
        query_platform_and_set_update_description_text(msg, result_id)

        return result


    schema = PlatformAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformAttachment,
        "methods": {"query": query},
    }


"""Module for the platform attachment detail resource."""


class PlatformAttachmentDetail(ResourceDetail):
    """
    Resource for platform attachments.

    Provides get, patch & delete methods.
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if PlatformAttachment not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)
    def after_patch(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["platform"]["data"]["id"]
        msg = "update;attachment"
        query_platform_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        device_attachment = (
            db.session.query(PlatformAttachment).filter_by(id=kwargs["id"]).one_or_none()
        )
        if device_attachment is None:
            raise ObjectNotFound("Object not found!")
        platform = device_attachment.get_parent()
        msg = "delete;attachment"
        set_update_description_text_and_update_by_user(platform, msg)

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """

        attachment = (
            db.session.query(PlatformAttachment).filter_by(id=kwargs["id"]).first()
        )
        if attachment is None:
            raise ObjectNotFound({"pointer": ""}, "Object Not Found")
        url = attachment.url
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError(
                "Deletion failed as the attachment is still in use.", str(e)
            )

        delete_attachments_in_minio_by_url(url)
        final_result = {"meta": {"message": "Object successfully deleted"}}

        return final_result

    schema = PlatformAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformAttachment,
    }
