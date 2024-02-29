# SPDX-FileCopyrightText:  2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Module for the site image resource classes."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Site, SiteAttachment, SiteImage
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.site_image_schema import SiteImageSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_site_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class SiteImageList(ResourceList):
    """Resource class for the list endpoint for site images."""

    def query(self, view_kwargs):
        """Return a (possibly) filtered query."""
        query_ = filter_visible(self.session.query(self.model))
        site_id = view_kwargs.get("site_id")
        if site_id is not None:
            site = self.session.query(Site).filter_by(id=site_id).first()
            if not site:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Site: {} not found".format(site_id),
                )
            query_ = query_.filter(SiteImage.site_id == site_id)

        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Run some hooks before creating the object."""
        existing_entry = (
            self.session.query(self.model)
            .filter_by(
                site_id=data.get("site"),
                attachment_id=data.get("attachment"),
            )
            .first()
        )
        if existing_entry:
            raise ConflictError(
                "There is already an image entry for the attachment for this site."
            )
        site = self.session.query(Site).filter_by(id=data.get("site")).first()
        attachment = (
            self.session.query(SiteAttachment)
            .filter_by(id=data.get("attachment"))
            .first()
        )
        if site and attachment:
            if not attachment.site_id == site.id:
                raise ConflictError("Site and Attachment doesn't belong to each other.")
        add_created_by_id(data)

    def after_post(self, result):
        """Run some hook after posting the data."""
        result_id = result[0]["data"]["relationships"]["site"]["data"]["id"]
        msg = "update;basic data"
        query_site_set_update_description_and_update_pidinst(msg, result_id)
        return result

    schema = SiteImageSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": SiteImage,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class SiteImageDetail(ResourceDetail):
    """Resource class for the site images."""

    def before_get(self, args, kwargs):
        """Run some hooks before getting the data."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some hooks before patching the data."""
        site_image_id = kwargs["id"]
        existing_site_image = (
            db.session.query(SiteImage).filter_by(id=site_image_id).first()
        )
        if existing_site_image:
            attachment_id = existing_site_image.attachment_id
            site_id = existing_site_image.site_id
            if "site" in data.keys():
                site_id = data["site"]
            if "attachment" in data.keys():
                attachment_id = data["attachment"]
            conflicting = (
                db.session.query(SiteImage)
                .filter_by(site_id=site_id, attachment_id=attachment_id)
                .filter(SiteImage.id != site_image_id)
                .first()
            )
            if conflicting:
                raise ConflictError(
                    "There is already an attachment as image for this site."
                )

            site = db.session.query(Site).filter_by(id=site_id).first()
            attachment = (
                db.session.query(SiteAttachment).filter_by(id=attachment_id).first()
            )
            if not attachment.site_id == site.id:
                raise ConflictError("Site and Attachment doesn't belong to each other.")

        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some hooks after the patch."""
        result_id = result["data"]["relationships"]["site"]["data"]["id"]
        msg = "update;basic data"
        query_site_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Run some hooks bfore deleting the data."""
        site_image = (
            db.session.query(SiteImage).filter_by(id=kwargs["id"]).one_or_none()
        )
        if site_image is None:
            raise ObjectNotFound("Object not found")

        msg = "update;basic data"
        set_update_description_text_user_and_pidinst(site_image.site, msg)

    schema = SiteImageSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": SiteImage,
    }
    permission_classes = [DelegateToCanFunctions]
