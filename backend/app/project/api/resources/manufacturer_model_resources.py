# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resource classes for the manufacturer models."""

from flask_rest_jsonapi import ResourceDetail, ResourceList

from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..models import ManufacturerModel
from ..models.base_model import db
from ..permissions.common import IsReadOnly
from ..schemas.manufacturer_model_schema import ManufacturerModelSchema
from .base_resource import check_if_object_not_found


class ManufacturerModelList(ResourceList):
    """List endpoint for the manufacturer models."""

    schema = ManufacturerModelSchema
    data_layer = {
        "session": db.session,
        "model": ManufacturerModel,
        "class": EsSqlalchemyDataLayer,
    }
    permission_classes = [IsReadOnly]


class ManufacturerModelDetail(ResourceDetail):
    """Detail endpoint for the manufacturer models."""

    def before_get(self, args, kwargs):
        """Query the object or raise 404 error."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = ManufacturerModelSchema
    data_layer = {
        "session": db.session,
        "model": ManufacturerModel,
    }
    permission_classes = [IsReadOnly]
