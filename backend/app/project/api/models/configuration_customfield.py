# SPDX-FileCopyrightText: 2023
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Model class for the configuration custom field."""

from .base_model import db
from .mixin import IndirectSearchableMixin


class ConfigurationCustomField(db.Model, IndirectSearchableMixin):
    """Custom field class for configurations."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(256), nullable=False)
    value = db.Column(db.String(1024), nullable=True)
    description = db.Column(db.Text, nullable=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        backref=db.backref(
            "configuration_customfields",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )

    def to_search_entry(self):
        """Transform to a dict to store into full text search index."""
        return {
            "key": self.key,
            "value": self.value,
            "description": self.description,
        }

    def get_parent_search_entities(self):
        """Return the configuration as parent entity."""
        return [self.configuration]

    def get_parent(self):
        """Return parent object."""
        return self.configuration
