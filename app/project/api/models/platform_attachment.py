"""Class for the platform attachment model."""

from sqlalchemy.ext.hybrid import hybrid_property

from .base_model import db
from .mixin import AuditMixin, IndirectSearchableMixin


class PlatformAttachment(db.Model, IndirectSearchableMixin, AuditMixin):
    """Platform attachment class."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    internal_url = db.Column(db.String(1024), nullable=True)
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    platform = db.relationship("Platform")

    @hybrid_property
    def is_upload(self):
        """Return True if the internal url is set."""
        return bool(self.internal_url)

    def to_search_entry(self):
        """Transform to en entry for the search index."""
        # to be included in the platform
        return {"label": self.label, "url": self.url}

    def get_parent_search_entities(self):
        """Return the platform as parent."""
        return [self.platform]

    def get_parent(self):
        """Return parent object."""
        return self.platform
