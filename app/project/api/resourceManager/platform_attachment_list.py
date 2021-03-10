"""Module for the platform attachment list resource."""
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.models.platform_attachment import PlatformAttachment
from project.api.schemas.platform_attachment_schema import PlatformAttachmentSchema
from project.api.token_checker import token_required


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
        query_ = self.session.query(PlatformAttachment)
        platform_id = view_kwargs.get("platform_id")

        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Platform: {} not found".format(platform_id),
                )
            else:
                query_ = query_.filter(PlatformAttachment.platform_id == platform_id)
        return query_

    schema = PlatformAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformAttachment,
        "methods": {
            "query": query,
        },
    }
