# SPDX-FileCopyrightText: 2022
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from .base_model import db
from .mixin import IndirectSearchableMixin


class ConfigurationCustomField(db.Model, IndirectSearchableMixin):
    """
    Custom Field class for Configurations
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(256), nullable=False)
    value = db.Column(db.String(1024), nullable=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship("Configuration")

    def to_search_entry(self):
        return {
            "key": self.key,
            "value": self.value,
        }

    def get_parent_search_entities(self):
        """Return the configuration as parent entity."""
        return [self.configuration]

    def get_parent(self):
        """Return parent object."""
        return self.configuration
