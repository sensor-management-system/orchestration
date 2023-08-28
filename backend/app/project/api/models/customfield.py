# SPDX-FileCopyrightText: 2020 - 2023
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Model class for the configuration custom field."""

from .base_model import db
from .mixin import IndirectSearchableMixin


class CustomField(db.Model, IndirectSearchableMixin):
    """Custom field class (for devices)."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(256), nullable=False)
    value = db.Column(db.String(1024), nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(
        "Device",
        backref=db.backref(
            "customfields", cascade="save-update, merge, delete, delete-orphan"
        ),
    )

    def to_search_entry(self):
        """Transform to a dict to store into full text search index."""
        return {
            "key": self.key,
            "value": self.value,
        }

    def get_parent_search_entities(self):
        """Return the device as parent entity."""
        return [self.device]

    def get_parent(self):
        """Return parent object."""
        return self.device
