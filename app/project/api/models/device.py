from project.api.models.base_model import db
from project.api.models.mixin import AuditMixin, SearchableMixin


class Device(db.Model, AuditMixin, SearchableMixin):
    """
    Device class
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=True)
    short_name = db.Column(db.String(256), nullable=False)
    long_name = db.Column(db.String(256), nullable=True)
    serial_number = db.Column(db.String(256), nullable=True)
    manufacturer_uri = db.Column(db.String(256), nullable=True)
    manufacturer_name = db.Column(db.String(256), nullable=True)
    dual_use = db.Column(db.Boolean, default=False)
    model = db.Column(db.String(256), nullable=True)
    inventory_number = db.Column(db.String(256), nullable=True)
    persistent_identifier = db.Column(db.String(256), nullable=True, unique=True)
    website = db.Column(db.String(1024), nullable=True)
    device_type_uri = db.Column(db.String(256), nullable=True)
    device_type_name = db.Column(db.String(256), nullable=True)
    status_uri = db.Column(db.String(256), nullable=True)
    status_name = db.Column(db.String(256), nullable=True)
    customfields = db.relationship(
        "CustomField", cascade="save-update, merge, delete, delete-orphan"
    )
    device_properties = db.relationship(
        "DeviceProperty", cascade="save-update, merge, delete, delete-orphan"
    )
    events = db.relationship(
        "Event", cascade="save-update, merge, delete, delete-orphan"
    )

    device_attachments = db.relationship(
        "DeviceAttachment", cascade="save-update, merge, delete, delete-orphan"
    )

    def to_search_entry(self):
        return {
            "short_name": self.short_name,
            "long_name": self.long_name,
            "description": self.description,
            "serial_number": self.serial_number,
            "manufacturer_name": self.manufacturer_name,
            "dual_use": self.dual_use,
            "model": self.model,
            "inventory_number": self.inventory_number,
            "persistent_identifier": self.persistent_identifier,
            "website": self.website,
            "device_type_name": self.device_type_name,
            "status_name": self.status_name,
            "attachments": [a.to_search_entry() for a in self.device_attachments],
            "contacts": [c.to_search_entry() for c in self.contacts],
            "properties": [p.to_search_entry() for p in self.device_properties],
            "customfields": [c.to_search_entry() for c in self.customfields],
        }
