# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Resource classes for the generic platform action attachments."""
from flask_rest_jsonapi import ResourceDetail, ResourceList

from ..models.base_model import db
from ..models.generic_action_attachments import GenericPlatformActionAttachment
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.generic_action_attachment_schema import (
    GenericPlatformActionAttachmentSchema,
)
from .base_resource import check_if_object_not_found
from .mixins.mqtt_notification import MqttNotificationMixin


class GenericPlatformActionAttachmentList(MqttNotificationMixin, ResourceList):
    """List resource class for the platform action attachments."""

    def query(self, view_kwargs):
        """Return the query with some prefilter."""
        return filter_visible(self.session.query(self.model))

    schema = GenericPlatformActionAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": GenericPlatformActionAttachment,
        "methods": {
            "query": query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class GenericPlatformActionAttachmentDetail(MqttNotificationMixin, ResourceDetail):
    """Detail resource class for the platform action attachments."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if GenericPlatformActionAttachment not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = GenericPlatformActionAttachmentSchema
    data_layer = {"session": db.session, "model": GenericPlatformActionAttachment}
    permission_classes = [DelegateToCanFunctions]
