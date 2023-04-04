"""Resource classes for the configuration action attachments."""

from flask_rest_jsonapi import ResourceDetail

from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.generic_action_attachments import GenericConfigurationActionAttachment
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.generic_action_attachment_schema import (
    GenericConfigurationActionAttachmentSchema,
)
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


class GenericConfigurationActionAttachmentList(ResourceList):
    """List resource class for the configuration action attachments."""

    def query(self, view_kwargs):
        """Return the query with some prefilter."""
        return filter_visible(self.session.query(self.model))

    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationActionAttachment,
        "methods": {
            "query": query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class GenericConfigurationActionAttachmentDetail(ResourceDetail):
    """Detail resource class for the configuration action attachments."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if GenericConfigurationActionAttachment not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericConfigurationActionAttachment}
    permission_classes = [DelegateToCanFunctions]
