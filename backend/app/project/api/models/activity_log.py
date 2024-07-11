# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Model to store any kind of activity in the SMS."""

import json

from .base_model import db
from .mixin import CreatedMixin


class ActivityLog(db.Model, CreatedMixin):
    """Log to store any kind of activity in the SMS."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entity = db.Column(db.String(256), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    data = db.Column(db.JSON(), nullable=True)

    @classmethod
    def create(cls, entity, user, description, data=None):
        """Create an activity log entry by using the entity."""
        if data is None:
            # If we don't explicity set the data, we load it from the
            # entry. We use the json serialization in order to ensure that
            # we are super save in storing it to the database - without any
            # further serialization issues.
            data = json.loads(json.dumps(entity.to_search_entry(), default=str))
        return cls(
            created_by_id=user.id,
            description=description,
            entity=type(entity).__name__,
            entity_id=entity.id,
            data=data,
        )
