"""Module for the device attachment list resource."""
from flask_rest_jsonapi import JsonApiException, ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..helpers.errors import ConflictError
from ..models.base_model import db
from ..models.device import Device
from ..models.device_attachment import DeviceAttachment
from ..schemas.device_attachment_schema import DeviceAttachmentSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    delete_attachments_in_minio_by_url,
    query_device_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
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
        query_ = get_query_with_permissions_for_related_objects(self.model)
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

    def after_post(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["device"]["data"]["id"]
        msg = "create;attachment"
        query_device_and_set_update_description_text(msg, result_id)

        return result

    schema = DeviceAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceAttachment,
        "methods": {"query": query},
    }


"""Module for the device attachment detail resource."""


class DeviceAttachmentDetail(ResourceDetail):
    """
    Resource for device attachments.

    Provides get, patch & delete methods.
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceAttachment not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def after_patch(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["device"]["data"]["id"]
        msg = "update;attachment"
        query_device_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Set the update description for the device if we delete the attachment."""
        device_attachment = (
            db.session.query(DeviceAttachment).filter_by(id=kwargs["id"]).one_or_none()
        )
        if device_attachment is None:
            raise ObjectNotFound("Object not found!")
        device = device_attachment.get_parent()
        msg = "delete;attachment"
        set_update_description_text_and_update_by_user(device, msg)

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

    schema = DeviceAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceAttachment,
    }
