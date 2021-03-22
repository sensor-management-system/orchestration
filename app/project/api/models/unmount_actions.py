from ..models.mixin import AuditMixin

from .base_model import db


class PlatformUnmountAction(db.Model, AuditMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref("platform_unmount_actions"),
    )
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    platform = db.relationship(
        "Platform",
        uselist=False,
        foreign_keys=[platform_id],
        backref=db.backref("platform_unmount_actions"),
    )
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("platform_unmount_actions"),
    )


class DeviceUnmountAction(db.Model, AuditMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref("device_unmount_actions"),
    )
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(
        "Device",
        uselist=False,
        foreign_keys=[device_id],
        backref=db.backref("device_unmount_actions"),
    )
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("device_unmount_actions"),
    )
