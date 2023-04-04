"""Resource classes for the generic platform action attachments."""
from flask_rest_jsonapi import ResourceDetail

from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.generic_action_attachments import GenericPlatformActionAttachment
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.generic_action_attachment_schema import (
    GenericPlatformActionAttachmentSchema,
)
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


class GenericPlatformActionAttachmentList(ResourceList):
    """List resource class for the platform action attachments."""

    def query(self, view_kwargs):
        """Return the query with some prefilter."""
        return filter_visible(self.session.query(self.model))

    schema = GenericPlatformActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericPlatformActionAttachment,
        "methods": {
            "query": query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class GenericPlatformActionAttachmentDetail(ResourceDetail):
    """Detail resource class for the platform action attachments."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if GenericPlatformActionAttachment not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = GenericPlatformActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericPlatformActionAttachment}
    permission_classes = [DelegateToCanFunctions]
