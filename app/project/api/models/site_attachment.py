# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Class for the attachment model for sites."""

from sqlalchemy.ext.hybrid import hybrid_property

from .base_model import db
from .mixin import AuditMixin, IndirectSearchableMixin


class SiteAttachment(db.Model, IndirectSearchableMixin, AuditMixin):
    """Site attachment class."""

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    internal_url = db.Column(db.String(1024), nullable=True)
    site_id = db.Column(db.Integer, db.ForeignKey("site.id"), nullable=False)
    site = db.relationship("Site")

    @hybrid_property
    def is_upload(self):
        """Return True if the internal url is used."""
        return bool(self.internal_url)

    def to_search_entry(self):
        """Transform the attachment for the search index."""
        # to be included in the sites
        return {"label": self.label, "url": self.url}

    def get_parent_search_entities(self):
        """Return the site as parent search entity."""
        return [self.site]

    def get_parent(self):
        """Return parent object."""
        return self.site
