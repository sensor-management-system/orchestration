"""Module for the platform attachment detail resource."""
from flask_rest_jsonapi import ResourceDetail, JsonApiException
from flask_rest_jsonapi.exceptions import ObjectNotFound

from .base_resource import delete_attachments_in_minio_by_url
from ..helpers.errors import ConflictError
from ..models.base_model import db
from ..models.platform_attachment import PlatformAttachment
from ..schemas.platform_attachment_schema import PlatformAttachmentSchema
from ..token_checker import token_required


class PlatformAttachmentDetail(ResourceDetail):
    """
    Resource for platform attachments.

    Provides get, patch & delete methods.
    """

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """

        attachment = (db.session.query(PlatformAttachment).filter_by(id=kwargs["id"]).first())
        if attachment is None:
            raise ObjectNotFound({'pointer': ''}, 'Object Not Found')
        url = attachment.url
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError("Deletion failed as the attachment is still in use.", str(e))

        delete_attachments_in_minio_by_url(url)
        final_result = {'meta': {'message': 'Object successfully deleted'}}

        return final_result

    schema = PlatformAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformAttachment,
    }
