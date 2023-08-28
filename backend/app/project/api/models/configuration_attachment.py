# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Class for the attachment model for configurations."""

from sqlalchemy.ext.hybrid import hybrid_property

from .base_model import db
from .mixin import AuditMixin, IndirectSearchableMixin


class ConfigurationAttachment(db.Model, IndirectSearchableMixin, AuditMixin):
    """Configuration attachment class."""

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    internal_url = db.Column(db.String(1024), nullable=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        backref=db.backref(
            "configuration_attachments",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )

    @hybrid_property
    def is_upload(self):
        """Return True if the internal url is used."""
        return bool(self.internal_url)

    def to_search_entry(self):
        """Transform the attachment for the search index."""
        # to be included in the configurations
        return {"label": self.label, "url": self.url}

    def get_parent_search_entities(self):
        """Return the configuration as parent search entity."""
        return [self.configuration]

    def get_parent(self):
        """Return parent object."""
        return self.configuration
