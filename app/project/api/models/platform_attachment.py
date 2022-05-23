from .base_model import db
from .mixin import IndirectSearchableMixin


class PlatformAttachment(db.Model):
    """
    Platform Attachment class
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    platform = db.relationship("Platform")

    def to_search_entry(self):
        # to be included in the platform
        return {"label": self.label, "url": self.url}

    def get_parent_search_entities(self):
        """Return the platform as parent."""
        return [self.platform]

    def get_parent(self):
        """Return parent object."""
        return self.platform
