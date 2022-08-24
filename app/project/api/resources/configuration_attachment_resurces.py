"""Module for the configuration attachments list resource."""
from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import JsonApiException, ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import (
    check_deletion_permission_for_configuration_related_objects,
    check_patch_permission_for_configuration_related_objects,
    check_permissions_for_configuration_related_objects,
    check_post_permission_for_configuration_related_objects,
    get_query_with_permissions_for_configuration_related_objects,
)
from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import decode_json_request_data
from ..models import Configuration, ConfigurationAttachment
from ..models.base_model import db
from ..schemas.configuration_attachment_schema import ConfigurationAttachmentSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    delete_attachments_in_minio_by_url,
    query_configuration_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
)


class ConfigurationAttachmentList(ResourceList):
    """
    List resource for configuration attachments.
    """

    def query(self, view_kwargs):
        """
        Query the entries from the database.
        """
        query_ = get_query_with_permissions_for_configuration_related_objects(
            self.model
        )
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

    def before_post(self, args, kwargs, data=None):
        check_post_permission_for_configuration_related_objects()

    def after_post(self, result):
        """
        Add update description to related configuraiton.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "create;attachment"
        query_configuration_and_set_update_description_text(msg, result_id)

        return result

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

    def before_get(self, args, kwargs):
        """Return 404 Responses if ConfigurationAttachment not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)
        check_permissions_for_configuration_related_objects(
            self._data_layer.model, kwargs["id"]
        )

    def before_patch(self, args, kwargs, data=None):
        check_patch_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )

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
        check_deletion_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )
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
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """

        attachment = (
            db.session.query(ConfigurationAttachment).filter_by(id=kwargs["id"]).first()
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

    schema = ConfigurationAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationAttachment,
    }
