# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Schema classes for the tsm endpoints."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class TsmEndpointSchema(Schema):
    """Schema class for the tsm endpoints."""

    class Meta:
        """Meta class for the schema."""

        type_ = "tsm_endpoint"
        self_view = "api.tsm_endpoint_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True)
    name = fields.String(required=True)
    url = fields.String(required=True)
