# SPDX-FileCopyrightText: 2020 - 2021
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from marshmallow import Schema as MarshmallowSchema
from marshmallow_jsonapi import fields


class AttachmentSchema(MarshmallowSchema):
    """
    This class create a schema for a attachment.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = "attachment"

    id = fields.Integer(as_string=True)
    label = fields.Str(allow_none=True)
    url = fields.Str(required=True)

    @staticmethod
    def dict_serializer(obj):
        """Convert the object to an dict."""
        if obj is not None:
            return {"label": obj.label, "url": obj.url}
