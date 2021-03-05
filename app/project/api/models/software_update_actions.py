from safrs import SAFRSBase

from project.api.models.base_model import db
from project.api.models.mixin import AuditMixin


class DeviceSoftwareUpdateAction(db.Model, AuditMixin, SAFRSBase):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(
        "Device",
        uselist=False,
        foreign_keys=[device_id],
        backref=db.backref("device_software_update_actions"),
    )
    software_type_name = db.Column(db.String(256), nullable=False)
    software_type_uri = db.Column(db.String(256), nullable=True)
    update_date = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(256), nullable=True)
    repository_url = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("device_software_update_actions"),
    )


class PlatformSoftwareUpdateAction(db.Model, AuditMixin, SAFRSBase):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    platform = db.relationship(
        "Platform",
        uselist=False,
        foreign_keys=[platform_id],
        backref=db.backref("platform_software_update_actions"),
    )
    software_type_name = db.Column(db.String(256), nullable=False)
    software_type_uri = db.Column(db.String(256), nullable=True)
    update_date = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(256), nullable=True)
    repository_url = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("platform_software_update_actions"),
    )
