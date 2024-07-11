# SPDX-FileCopyrightText:  2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Module for the platform image resource classes."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Platform, PlatformAttachment, PlatformImage
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.platform_image_schema import PlatformImageSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_platform_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class PlatformImageList(ResourceList):
    """Resource class for the list endpoint for platform images."""

    def query(self, view_kwargs):
        """Return a (possibly) filtered query."""
        query_ = filter_visible(self.session.query(self.model))
        platform_id = view_kwargs.get("platform_id")
        if platform_id is not None:
            platform = self.session.query(Platform).filter_by(id=platform_id).first()
            if not platform:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Platform: {} not found".format(platform_id),
                )
            query_ = query_.filter(PlatformImage.platform_id == platform_id)

        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Run some hooks before creating the object."""
        existing_entry = (
            self.session.query(self.model)
            .filter_by(
                platform_id=data.get("platform"),
                attachment_id=data.get("attachment"),
            )
            .first()
        )
        if existing_entry:
            raise ConflictError(
                "There is already an image entry for the attachment for this platform."
            )
        platform = (
            self.session.query(Platform).filter_by(id=data.get("platform")).first()
        )
        attachment = (
            self.session.query(PlatformAttachment)
            .filter_by(id=data.get("attachment"))
            .first()
        )
        if platform and attachment:
            if not attachment.platform_id == platform.id:
                raise ConflictError(
                    "Platform and Attachment doesn't belong to each other."
                )
        add_created_by_id(data)

    def after_post(self, result):
        """Run some hook after posting the data."""
        result_id = result[0]["data"]["relationships"]["platform"]["data"]["id"]
        msg = "update;basic data"
        query_platform_set_update_description_and_update_pidinst(msg, result_id)
        return result

    schema = PlatformImageSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformImage,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class PlatformImageDetail(ResourceDetail):
    """Resource class for the platform images."""

    def before_get(self, args, kwargs):
        """Run some hooks before getting the data."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some hooks before patching the data."""
        platform_image_id = kwargs["id"]
        existing_platform_image = (
            db.session.query(PlatformImage).filter_by(id=platform_image_id).first()
        )
        if existing_platform_image:
            attachment_id = existing_platform_image.attachment_id
            platform_id = existing_platform_image.platform_id
            if "platform" in data.keys():
                platform_id = data["platform"]
            if "attachment" in data.keys():
                attachment_id = data["attachment"]
            conflicting = (
                db.session.query(PlatformImage)
                .filter_by(platform_id=platform_id, attachment_id=attachment_id)
                .filter(PlatformImage.id != platform_image_id)
                .first()
            )
            if conflicting:
                raise ConflictError(
                    "There is already an attachment as image for this platform."
                )

            platform = db.session.query(Platform).filter_by(id=platform_id).first()
            attachment = (
                db.session.query(PlatformAttachment).filter_by(id=attachment_id).first()
            )
            if not attachment.platform_id == platform.id:
                raise ConflictError(
                    "Platform and Attachment doesn't belong to each other."
                )

        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some hooks after the patch."""
        result_id = result["data"]["relationships"]["platform"]["data"]["id"]
        msg = "update;basic data"
        query_platform_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Run some hooks bfore deleting the data."""
        platform_image = (
            db.session.query(PlatformImage).filter_by(id=kwargs["id"]).one_or_none()
        )
        if platform_image is None:
            raise ObjectNotFound("Object not found")

        msg = "update;basic data"
        set_update_description_text_user_and_pidinst(platform_image.platform, msg)

    schema = PlatformImageSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformImage,
    }
    permission_classes = [DelegateToCanFunctions]
