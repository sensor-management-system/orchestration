from sqlalchemy import UniqueConstraint
from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.device import Device
from project.api.models.mixin import AuditMixin
from project.api.models.platform import Platform


class ConfigurationDevice(db.Model, AuditMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    offset_x = db.Column(db.Float(), nullable=True)
    offset_y = db.Column(db.Float(), nullable=True)
    offset_z = db.Column(db.Float(), nullable=True)
    calibration_date = db.Column(db.DateTime, nullable=True)

    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        Configuration, uselist=False, foreign_keys=[configuration_id]
    )

    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(Device, uselist=False, foreign_keys=[device_id])

    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    platform = db.relationship(Platform, uselist=False, foreign_keys=[platform_id])

    __table_args__ = (
        UniqueConstraint(
            "device_id", "configuration_id", name="uc_configuration_device"
        ),
    )
