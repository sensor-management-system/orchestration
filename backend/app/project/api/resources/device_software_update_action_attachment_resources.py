# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Resource classes for the device software update action attachments."""

from flask_rest_jsonapi import ResourceDetail, ResourceList

from ..models.base_model import db
from ..models.software_update_action_attachments import (
    DeviceSoftwareUpdateActionAttachment,
)
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.software_update_action_attachment_schema import (
    DeviceSoftwareUpdateActionAttachmentSchema,
)
from .base_resource import check_if_object_not_found


class DeviceSoftwareUpdateActionAttachmentList(ResourceList):
    """List resource class for the device software update action attachments."""

    def query(self, view_kwargs):
        """Return the query with some prefilter."""
        return filter_visible(self.session.query(self.model))

    schema = DeviceSoftwareUpdateActionAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": DeviceSoftwareUpdateActionAttachment,
        "methods": {"query": query},
    }
    permission_classes = [DelegateToCanFunctions]


class DeviceSoftwareUpdateActionAttachmentDetail(ResourceDetail):
    """Detail resource class for the device software update action attachments."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceSoftwareUpdateActionAttachment not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = DeviceSoftwareUpdateActionAttachmentSchema
    data_layer = {"session": db.session, "model": DeviceSoftwareUpdateActionAttachment}
    permission_classes = [DelegateToCanFunctions]
