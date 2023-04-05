# SPDX-FileCopyrightText: 2020 - 2022
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from .base_model import db
from .mixin import IndirectSearchableMixin


class CustomField(db.Model, IndirectSearchableMixin):
    """
    Custom Field class
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(256), nullable=False)
    value = db.Column(db.String(1024), nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship("Device")

    def to_search_entry(self):
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
