"""Class for the device attachment model."""
from sqlalchemy.ext.hybrid import hybrid_property

from .base_model import db
from .mixin import IndirectSearchableMixin


class DeviceAttachment(db.Model, IndirectSearchableMixin):
    """Device attachment class."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    internal_url = db.Column(db.String(1024), nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship("Device")

    @hybrid_property
    def is_upload(self):
        """Return True if the internal url is set."""
        return bool(self.internal_url)

    def to_search_entry(self):
        """Transform to an entry for the search index."""
        # to be included in the devices
        return {"label": self.label, "url": self.url}

    def get_parent_search_entities(self):
        """Return the device as parent search entity."""
        return [self.device]

    def get_parent(self):
        """Return parent object."""
        return self.device
