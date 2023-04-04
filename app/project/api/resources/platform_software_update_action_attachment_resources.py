"""Resource classes for platform software update action attachments."""
from flask_rest_jsonapi import ResourceDetail

from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.software_update_action_attachments import (
    PlatformSoftwareUpdateActionAttachment,
)
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.software_update_action_attachment_schema import (
    PlatformSoftwareUpdateActionAttachmentSchema,
)
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


class PlatformSoftwareUpdateActionAttachmentList(ResourceList):
    """List resource class for platform software update action attachments."""

    def query(self, view_kwargs):
        """Return the query with some prefilter."""
        return filter_visible(self.session.query(self.model))

    schema = PlatformSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateActionAttachment,
        "methods": {
            "query": query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class PlatformSoftwareUpdateActionAttachmentDetail(ResourceDetail):
    """Detail resource class for platform software update action attachments."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if PlatformSoftwareUpdateActionAttachment not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = PlatformSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateActionAttachment,
    }
    permission_classes = [DelegateToCanFunctions]
