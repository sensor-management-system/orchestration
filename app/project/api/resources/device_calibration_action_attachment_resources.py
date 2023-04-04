"""Resource classes for device calibration attachments."""
from flask_rest_jsonapi import ResourceDetail

from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.calibration_attachments import DeviceCalibrationAttachment
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.calibration_action_attachment_schema import (
    DeviceCalibrationAttachmentSchema,
)
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


class DeviceCalibrationAttachmentList(ResourceList):
    """List resource for device calibration attachments."""

    def query(self, view_kwargs):
        """Return the query with some prefilter."""
        query_ = filter_visible(self.session.query(self.model))
        return query_

    schema = DeviceCalibrationAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceCalibrationAttachment,
        "methods": {
            "query": query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class DeviceCalibrationAttachmentDetail(ResourceDetail):
    """Detail resource for device calibration attachments."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceCalibrationAttachment not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = DeviceCalibrationAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceCalibrationAttachment}
    permission_classes = [DelegateToCanFunctions]
