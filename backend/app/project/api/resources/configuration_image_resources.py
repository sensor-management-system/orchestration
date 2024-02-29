# SPDX-FileCopyrightText:  2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Module for the configuration image resource classes."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Configuration, ConfigurationAttachment, ConfigurationImage
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.configuration_image_schema import ConfigurationImageSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_configuration_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class ConfigurationImageList(ResourceList):
    """Resource class for the list endpoint for configuration images."""

    def query(self, view_kwargs):
        """Return a (possibly) filtered query."""
        query_ = filter_visible(self.session.query(self.model))
        configuration_id = view_kwargs.get("configuration_id")
        if configuration_id is not None:
            configuration = (
                self.session.query(Configuration).filter_by(id=configuration_id).first()
            )
            if not configuration:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Configuration: {} not found".format(configuration_id),
                )
            query_ = query_.filter(
                ConfigurationImage.configuration_id == configuration_id
            )

        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Run some hooks before creating the object."""
        existing_entry = (
            self.session.query(self.model)
            .filter_by(
                configuration_id=data.get("configuration"),
                attachment_id=data.get("attachment"),
            )
            .first()
        )
        if existing_entry:
            raise ConflictError(
                "There is already an image entry for the attachment for this configuration."
            )
        configuration = (
            self.session.query(Configuration)
            .filter_by(id=data.get("configuration"))
            .first()
        )
        attachment = (
            self.session.query(ConfigurationAttachment)
            .filter_by(id=data.get("attachment"))
            .first()
        )
        if configuration and attachment:
            if not attachment.configuration_id == configuration.id:
                raise ConflictError(
                    "Configuration and Attachment doesn't belong to each other."
                )
        add_created_by_id(data)

    def after_post(self, result):
        """Run some hook after posting the data."""
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "update;basic data"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)
        return result

    schema = ConfigurationImageSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationImage,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class ConfigurationImageDetail(ResourceDetail):
    """Resource class for the configuration images."""

    def before_get(self, args, kwargs):
        """Run some hooks before getting the data."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some hooks before patching the data."""
        configuration_image_id = kwargs["id"]
        existing_configuration_image = (
            db.session.query(ConfigurationImage)
            .filter_by(id=configuration_image_id)
            .first()
        )
        if existing_configuration_image:
            attachment_id = existing_configuration_image.attachment_id
            configuration_id = existing_configuration_image.configuration_id
            if "configuration" in data.keys():
                configuration_id = data["configuration"]
            if "attachment" in data.keys():
                attachment_id = data["attachment"]
            conflicting = (
                db.session.query(ConfigurationImage)
                .filter_by(
                    configuration_id=configuration_id, attachment_id=attachment_id
                )
                .filter(ConfigurationImage.id != configuration_image_id)
                .first()
            )
            if conflicting:
                raise ConflictError(
                    "There is already an attachment as image for this configuration."
                )

            configuration = (
                db.session.query(Configuration).filter_by(id=configuration_id).first()
            )
            attachment = (
                db.session.query(ConfigurationAttachment)
                .filter_by(id=attachment_id)
                .first()
            )
            if not attachment.configuration_id == configuration.id:
                raise ConflictError(
                    "Configuration and Attachment doesn't belong to each other."
                )

        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some hooks after the patch."""
        result_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "update;basic data"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Run some hooks bfore deleting the data."""
        configuration_image = (
            db.session.query(ConfigurationImage)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if configuration_image is None:
            raise ObjectNotFound("Object not found")

        msg = "update;basic data"
        set_update_description_text_user_and_pidinst(
            configuration_image.configuration, msg
        )

    schema = ConfigurationImageSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationImage,
    }
    permission_classes = [DelegateToCanFunctions]
