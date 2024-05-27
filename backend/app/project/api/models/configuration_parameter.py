# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Model for configuration parameter."""

from .base_model import db
from .configuration import Configuration
from .mixin import AuditMixin, IndirectSearchableMixin


class ConfigurationParameter(db.Model, IndirectSearchableMixin, AuditMixin):
    """ConfigurationParameter class."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        Configuration,
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref(
            "configuration_parameters",
            cascade="save-update, merge, delete, delete-orphan",
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
        }

    def get_parent_search_entities(self):
        """Return the configuration as parent search entity."""
        return [self.configuration]
