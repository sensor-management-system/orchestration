from project.api.models.base_model import db
from project.api.models.mixin import AuditMixin
from sqlalchemy import UniqueConstraint


class ConfigurationDevice(db.Model, AuditMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    offset_x = db.Column(db.Float(), nullable=True)
    offset_y = db.Column(db.Float(), nullable=True)
    offset_z = db.Column(db.Float(), nullable=True)
    calibration_date = db.Column(db.DateTime, nullable=True)
    firmware_version = db.Column(db.String(256), nullable=True)

    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        backref=db.backref(
            "configuration_devices",
            cascade="all, save-update, merge, delete, delete-orphan",
        ),
        cascade="all",
    )
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(
        "Device", backref=db.backref("configuration_device", cascade="all")
    )
    parent_platform_id = db.Column(
        db.Integer, db.ForeignKey("platform.id"), nullable=False
    )
    parent_platform = db.relationship(
        "Platform", backref=db.backref("inner_configuration_device", cascade="all")
    )

    __table_args__ = (
        UniqueConstraint(
            "device_id", "configuration_id", name="uc_configuration_device"
        ),
    )
