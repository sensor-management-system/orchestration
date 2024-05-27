# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Model for the device parameter change."""
from .base_model import db
from .mixin import AuditMixin, IndirectSearchableMixin


class DeviceParameterValueChangeAction(db.Model, AuditMixin, IndirectSearchableMixin):
    """Class to represent a change in an device parameter value."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_parameter_id = db.Column(
        db.Integer, db.ForeignKey("device_parameter.id"), nullable=False
    )
    device_parameter = db.relationship(
        "DeviceParameter",
        uselist=False,
        foreign_keys=[device_parameter_id],
        backref=db.backref(
            "device_parameter_value_change_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    value = db.Column(db.Text, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship("Contact", uselist=False, foreign_keys=[contact_id])
    description = db.Column(db.Text, nullable=True)

    def to_search_entry(self):
        """Transform to a dict to store into full text search index."""
        return {
            "value": self.value,
            "description": self.description,
        }

    def get_parent_search_entities(self):
        """Return the device as parent search entity."""
        return [self.device_parameter.device]
