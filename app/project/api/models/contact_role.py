"""
Contact role models for devices, platforms & configurations.

The contact roles are reference tables between contacts and our main sms
models (device, platform, configuration).
Additionally they add a "role", which indicates that the contact is for that
device.
Examples for roles can be Manufacturer, Operator, Owner, or similar.
NERC for example defines some of them here:
http://vocab.nerc.ac.uk/collection/W08/current/
"""
from .base_model import db
from .mixin import IndirectSearchableMixin


class Role:
    """Base class for more specific role implementations."""

    role_name = db.Column(db.String, nullable=False)
    role_uri = db.Column(db.String(256), nullable=True)

    def to_search_entry(self):
        """Transform the model to an entry tos store in full text search."""
        return {
            "role_name": self.role_name,
            "role_uri": self.role_uri,
            # This comes from the specific classes.
            # However, currently they all have a contact relationship
            # (but all with a different backref name).
            "contact": self.contact.to_search_entry(),
        }


class DeviceContactRole(db.Model, Role, IndirectSearchableMixin):
    """Contact role for a device."""

    id = db.Column(db.Integer, primary_key=True)
    contact = db.relationship("Contact", backref="contact_device_roles")
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    device = db.relationship("Device", backref="device_contact_roles")
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"))

    def get_parent_search_entities(self):
        """Return the device."""
        return [self.device]

    def get_parent(self):
        """Return the parent object (for permission management)."""
        return self.device


class PlatformContactRole(db.Model, Role, IndirectSearchableMixin):
    """Contact role for a platform."""

    id = db.Column(db.Integer, primary_key=True)
    contact = db.relationship("Contact", backref="contact_platform_roles")
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    platform = db.relationship("Platform", backref="platform_contact_roles")
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"))

    def get_parent_search_entities(self):
        """Return the platform."""
        return [self.platform]

    def get_parent(self):
        """Return the parent object (for permission management)."""
        return self.platform


class ConfigurationContactRole(db.Model, Role, IndirectSearchableMixin):
    """Contact role for a configuration."""

    id = db.Column(db.Integer, primary_key=True)
    contact = db.relationship("Contact", backref="contact_configuration_roles")
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    configuration = db.relationship(
        "Configuration", backref="configuration_contact_roles"
    )
    configuration_id = db.Column(db.Integer, db.ForeignKey("configuration.id"))

    def get_parent_search_entities(self):
        """Return the configuration."""
        return [self.configuration]

    def get_parent(self):
        """Return the parent object (for permission management)."""
        return self.configuration
