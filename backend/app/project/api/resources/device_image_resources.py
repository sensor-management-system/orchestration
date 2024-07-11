# SPDX-FileCopyrightText:  2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Module for the device image resource classes."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Device, DeviceAttachment, DeviceImage
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.device_image_schema import DeviceImageSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_device_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class DeviceImageList(ResourceList):
    """Resource class for the list endpoint for device images."""

    def query(self, view_kwargs):
        """Return a (possibly) filtered query."""
        query_ = filter_visible(self.session.query(self.model))
        device_id = view_kwargs.get("device_id")
        if device_id is not None:
            device = self.session.query(Device).filter_by(id=device_id).first()
            if not device:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device: {} not found".format(device_id),
                )
            query_ = query_.filter(DeviceImage.device_id == device_id)

        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Run some hooks before creating the object."""
        existing_entry = (
            self.session.query(self.model)
            .filter_by(
                device_id=data.get("device"),
                attachment_id=data.get("attachment"),
            )
            .first()
        )
        if existing_entry:
            raise ConflictError(
                "There is already an image entry for the attachment for this device."
            )
        device = self.session.query(Device).filter_by(id=data.get("device")).first()
        attachment = (
            self.session.query(DeviceAttachment)
            .filter_by(id=data.get("attachment"))
            .first()
        )
        if device and attachment:
            if not attachment.device_id == device.id:
                raise ConflictError(
                    "Device and Attachment doesn't belong to each other."
                )
        add_created_by_id(data)

    def after_post(self, result):
        """Run some hook after posting the data."""
        result_id = result[0]["data"]["relationships"]["device"]["data"]["id"]
        msg = "update;basic data"
        query_device_set_update_description_and_update_pidinst(msg, result_id)
        return result

    schema = DeviceImageSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceImage,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class DeviceImageDetail(ResourceDetail):
    """Resource class for the device images."""

    def before_get(self, args, kwargs):
        """Run some hooks before getting the data."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some hooks before patching the data."""
        device_image_id = kwargs["id"]
        existing_device_image = (
            db.session.query(DeviceImage).filter_by(id=device_image_id).first()
        )
        if existing_device_image:
            attachment_id = existing_device_image.attachment_id
            device_id = existing_device_image.device_id
            if "device" in data.keys():
                device_id = data["device"]
            if "attachment" in data.keys():
                attachment_id = data["attachment"]
            conflicting = (
                db.session.query(DeviceImage)
                .filter_by(device_id=device_id, attachment_id=attachment_id)
                .filter(DeviceImage.id != device_image_id)
                .first()
            )
            if conflicting:
                raise ConflictError(
                    "There is already an attachment as image for this device."
                )

            device = db.session.query(Device).filter_by(id=device_id).first()
            attachment = (
                db.session.query(DeviceAttachment).filter_by(id=attachment_id).first()
            )
            if not attachment.device_id == device.id:
                raise ConflictError(
                    "Device and Attachment doesn't belong to each other."
                )

        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some hooks after the patch."""
        result_id = result["data"]["relationships"]["device"]["data"]["id"]
        msg = "update;basic data"
        query_device_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Run some hooks bfore deleting the data."""
        device_image = (
            db.session.query(DeviceImage).filter_by(id=kwargs["id"]).one_or_none()
        )
        if device_image is None:
            raise ObjectNotFound("Object not found")

        msg = "update;basic data"
        set_update_description_text_user_and_pidinst(device_image.device, msg)

    schema = DeviceImageSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceImage,
    }
    permission_classes = [DelegateToCanFunctions]
