from .base_model import db


class Role:
    role_name = db.Column(db.String, nullable=False)
    role_uri = db.Column(db.String(256), nullable=True)


class DeviceContactRole(db.Model, Role):
    """DeviceContactRole Role"""

    id = db.Column(db.Integer, primary_key=True)
    contact = db.relationship("Contact", backref="contact_device_roles")
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    device = db.relationship("Device", backref="device_contact_roles")
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"))


class PlatformContactRole(db.Model, Role):
    """PlatformContactRole Role"""

    id = db.Column(db.Integer, primary_key=True)
    contact = db.relationship("Contact", backref="contact_platform_roles")
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    platform = db.relationship("Platform", backref="platform_contact_roles")
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"))


class ConfigurationContactRole(db.Model, Role):
    """ConfigurationContactRole Role"""

    id = db.Column(db.Integer, primary_key=True)
    contact = db.relationship("Contact", backref="contact_configuration_roles")
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    configuration = db.relationship("Configuration", backref="configuration_contact_roles")
    configuration_id = db.Column(db.Integer, db.ForeignKey("configuration.id"))
