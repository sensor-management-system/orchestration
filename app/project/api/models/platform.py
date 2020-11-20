from project.api.models.base_model import db
from project.api.models.mixin import AuditMixin, SearchableMixin


class Platform(db.Model, AuditMixin, SearchableMixin):
    """
    Platform class
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=True)
    short_name = db.Column(db.String(256), nullable=False)
    long_name = db.Column(db.String(256), nullable=True)
    manufacturer_uri = db.Column(db.String(256), nullable=True)
    manufacturer_name = db.Column(db.String(256), nullable=True)
    model = db.Column(db.String(256), nullable=True)
    platform_type_uri = db.Column(db.String(256), nullable=True)
    platform_type_name = db.Column(db.String(256), nullable=True)
    status_uri = db.Column(db.String(256), nullable=True)
    status_name = db.Column(db.String(256), nullable=True)
    website = db.Column(db.String(1024), nullable=True)
    inventory_number = db.Column(db.String(256), nullable=True)
    serial_number = db.Column(db.String(256), nullable=True)
    persistent_identifier = db.Column(db.String(256), nullable=True, unique=True)
    platform_attachments = db.relationship(
        "PlatformAttachment", cascade="save-update, merge, delete, delete-orphan"
    )

    def to_search_entry(self):
        return {
            "short_name": self.short_name,
            "long_name": self.long_name,
            "description": self.description,
            "manufacturer_name": self.manufacturer_name,
            "model": self.model,
            "platform_type_name": self.platform_type_name,
            "status_name": self.status_name,
            "website": self.website,
            "inventory_number": self.inventory_number,
            "serial_number": self.serial_number,
            "persistent_identifier": self.persistent_identifier,
            "attachements": [a.to_search_entry() for a in self.platform_attachments],
            "contacts": [c.to_search_entry() for c in self.contacts],
        }
