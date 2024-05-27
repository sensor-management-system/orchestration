# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Model for the configuration parameter change."""
from .base_model import db
from .mixin import AuditMixin, IndirectSearchableMixin


class ConfigurationParameterValueChangeAction(
    db.Model, AuditMixin, IndirectSearchableMixin
):
    """Class to represent a change in an configuration parameter value."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_parameter_id = db.Column(
        db.Integer, db.ForeignKey("configuration_parameter.id"), nullable=False
    )
    configuration_parameter = db.relationship(
        "ConfigurationParameter",
        uselist=False,
        foreign_keys=[configuration_parameter_id],
        backref=db.backref(
            "configuration_parameter_value_change_actions",
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
        """Return the configuration as parent search entity."""
        return [self.configuration_parameter.configuration]
