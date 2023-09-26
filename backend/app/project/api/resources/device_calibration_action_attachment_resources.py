# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resource classes for device calibration attachments."""
from flask_rest_jsonapi import ResourceDetail, ResourceList

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
