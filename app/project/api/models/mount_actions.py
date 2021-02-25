from project.api.models.base_model import db
from project.api.models.mixin import AuditMixin


class PlatformMountAction(db.Model, AuditMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration", uselist=False, foreign_keys=[configuration_id]
    )
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    platform = db.relationship(
        "Platform",
        uselist=False,
        foreign_keys=["platform_id"],
        backref=db.backref("platform_mount_actions"),
    )
    parent_platform_id = db.Column(
        db.Integer, db.ForeignKey("platform.id"), nullable=True
    )
    parent_platform = db.relationship(
        "Platform",
        uselist=False,
        foreign_keys=["platform_id"],
        backref=db.backref("outer_platform_mount_actions"),
    )
    begin_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship("Contact", uselist=False, foreign_keys=[contact_id])
    offset_x = db.Column(db.Float, default=0)
    offset_y = db.Column(db.Float, default=0)
    offset_z = db.Column(db.Float, default=0)


class DeviceMountAction(db.Model, AuditMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration", uselist=False, foreign_keys=[configuration_id]
    )
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship("Device", uselist=False, foreign_keys=["device_id"])
    parent_platform_id = db.Column(
        db.Integer, db.ForeignKey("platform.id"), nullable=True
    )
    parent_platform = db.relationship(
        "Platform", uselist=False, foreign_keys=["platform_id"]
    )
    begin_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship("Contact", uselist=False, foreign_keys=[contact_id])
    offset_x = db.Column(db.Float, default=0)
    offset_y = db.Column(db.Float, default=0)
    offset_z = db.Column(db.Float, default=0)
