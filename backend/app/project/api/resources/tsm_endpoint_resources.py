# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resource classes for the tsm endpoints."""

from flask_rest_jsonapi import ResourceDetail, ResourceList

from ..models import TsmEndpoint
from ..models.base_model import db
from ..permissions.common import IsReadOnly
from ..schemas.tsm_endpoint_schema import TsmEndpointSchema
from .base_resource import check_if_object_not_found


class TsmEndpointList(ResourceList):
    """List endpoint for the tsm endpoints."""

    schema = TsmEndpointSchema
    data_layer = {
        "session": db.session,
        "model": TsmEndpoint,
    }
    permission_classes = [IsReadOnly]


class TsmEndpointDetail(ResourceDetail):
    """Detail endpoint for the tsm endpoints."""

    def before_get(self, args, kwargs):
        """Run some tests before the get method."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = TsmEndpointSchema
    data_layer = {
        "session": db.session,
        "model": TsmEndpoint,
    }
    permission_classes = [IsReadOnly]
