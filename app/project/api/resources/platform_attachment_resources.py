"""Module for the platform attachment list resource."""
from flask_rest_jsonapi import ResourceDetail, JsonApiException
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from .base_resource import delete_attachments_in_minio_by_url, check_if_object_not_found
from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..helpers.errors import ConflictError
from ..models.base_model import db
from ..models.platform import Platform
from ..models.platform_attachment import PlatformAttachment
from ..schemas.platform_attachment_schema import PlatformAttachmentSchema
from ..token_checker import token_required


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
