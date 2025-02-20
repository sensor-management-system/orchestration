# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Resource classes for device calibration attachments."""
from flask_rest_jsonapi import ResourceDetail, ResourceList

from ..models.base_model import db
from ..models.calibration_attachments import DeviceCalibrationAttachment
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.calibration_action_attachment_schema import (
    DeviceCalibrationAttachmentSchema,
)
from .base_resource import check_if_object_not_found
from .mixins.mqtt_notification import MqttNotificationMixin


class DeviceCalibrationAttachmentList(MqttNotificationMixin, ResourceList):
    """List resource for device calibration attachments."""

    def query(self, view_kwargs):
        """Return the query with some prefilter."""
        query_ = filter_visible(self.session.query(self.model))
        return query_

    schema = DeviceCalibrationAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": DeviceCalibrationAttachment,
        "methods": {
            "query": query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class DeviceCalibrationAttachmentDetail(MqttNotificationMixin, ResourceDetail):
    """Detail resource for device calibration attachments."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceCalibrationAttachment not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = DeviceCalibrationAttachmentSchema
    data_layer = {"session": db.session, "model": DeviceCalibrationAttachment}
    permission_classes = [DelegateToCanFunctions]
