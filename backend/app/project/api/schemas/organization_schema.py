# SPDX-FileCopyrightText: 2026
# - Nils Brinckmann <nils.brinckmann@gfz.de>
# - GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Schema class for the organization."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema


class OrganizationSchema(Schema):
    """Schema for the organization models."""

    class Meta:
        """Metaclass for the OrganizationSchema."""

        type_ = "organization"
        self_view = "api.organization_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "api.organization_list"

    id = fields.Integer(as_string=True)
    name = fields.Str(required=True)
    ror = fields.Str(allow_none=True)
    abbreviation = fields.Str(allow_none=True)
