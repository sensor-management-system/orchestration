# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Model for the platform parameter change."""
from .base_model import db
from .mixin import AuditMixin, IndirectSearchableMixin


class PlatformParameterValueChangeAction(db.Model, AuditMixin, IndirectSearchableMixin):
    """Class to represent a change in an platform parameter value."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform_parameter_id = db.Column(
        db.Integer, db.ForeignKey("platform_parameter.id"), nullable=False
    )
    platform_parameter = db.relationship(
        "PlatformParameter",
        uselist=False,
        foreign_keys=[platform_parameter_id],
        backref=db.backref(
            "platform_parameter_value_change_actions",
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
        """Return the platform as parent search entity."""
        return [self.platform_parameter.platform]
