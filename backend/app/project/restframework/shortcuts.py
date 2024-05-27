# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Some shortcuts for the views."""

from ..api.helpers.errors import NotFoundError
from ..api.models.base_model import db


def get_object_or_404(model, ident):
    """Mimiks the django get_object_or_404 shortcut function."""
    object = db.session.query(model).get(ident)
    if not object:
        raise NotFoundError("Object not found!")
    return object
