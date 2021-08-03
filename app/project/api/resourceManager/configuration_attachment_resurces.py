"""Module for the configuration attachments list resource."""
from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound, JsonApiException
from sqlalchemy.orm.exc import NoResultFound

from .base_resource import delete_attachments_in_minio_by_url
from ..helpers.errors import ConflictError
from ..models import Configuration, ConfigurationAttachment
from ..models.base_model import db
from ..schemas.configuration_attachment_schema import ConfigurationAttachmentSchema
from ..token_checker import token_required


class ConfigurationAttachmentList(ResourceList):
    """
    List resource for configuration attachments.
    """

    def query(self, view_kwargs):
        """
        Query the entries from the database.
        """
        query_ = self.session.query(ConfigurationAttachment)
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

    schema = ConfigurationAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationAttachment,
        "methods": {
            "query": query,
        },
    }


class ConfigurationAttachmentDetail(ResourceDetail):
    """
    Resource for ConfigurationAttachments.
    """

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """

        attachment = (db.session.query(ConfigurationAttachment).filter_by(id=kwargs["id"]).first())
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

    schema = ConfigurationAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationAttachment,
    }


class ConfigurationAttachmentRelationship(ResourceRelationship):
    """
    Relationship resource for ConfigurationAttachments.
    """

    schema = ConfigurationAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationAttachment,
    }
