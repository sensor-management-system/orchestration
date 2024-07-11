# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Model for device parameter."""

from .base_model import db
from .device import Device
from .mixin import AuditMixin, IndirectSearchableMixin


class DeviceParameter(db.Model, IndirectSearchableMixin, AuditMixin):
    """DeviceParameter class."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(
        Device,
        uselist=False,
        foreign_keys=[device_id],
        backref=db.backref(
            "device_parameters", cascade="save-update, merge, delete, delete-orphan"
        ),
    )
    label = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=True)
    unit_uri = db.Column(db.String(256), nullable=True)
    unit_name = db.Column(db.String(256), nullable=True)

    def to_search_entry(self):
        """Transform to a dict to store into full text search index."""
        return {
            "label": self.label,
            "description": self.description,
            "unit_uri": self.unit_uri,
            "unit_name": self.unit_name,
            "device_parameter_value_change_actions": [
                c.to_search_entry() for c in self.device_parameter_value_change_actions
            ],
        }

    def get_parent_search_entities(self):
        """Return the device as parent search entity."""
        return [self.device]
