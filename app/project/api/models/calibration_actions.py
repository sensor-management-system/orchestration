from .base_model import db
from .mixin import AuditMixin


class DeviceCalibrationAction(db.Model, AuditMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=True)
    current_calibration_date = db.Column(db.DateTime, nullable=False)
    next_calibration_date = db.Column(db.DateTime, nullable=True)
    formula = db.Column(db.String(256), nullable=True)
    value = db.Column(db.Float, nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(
        "Device",
        uselist=False,
        foreign_keys=[device_id],
        backref=db.backref(
            "device_calibration_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("device_calibration_actions"),
    )

    def get_parent(self):
        """Return parent object."""
        return self.device


class DevicePropertyCalibration(db.Model, AuditMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    calibration_action_id = db.Column(
        db.Integer, db.ForeignKey("device_calibration_action.id"), nullable=False
    )
    calibration_action = db.relationship(
        "DeviceCalibrationAction",
        uselist=False,
        foreign_keys=[calibration_action_id],
        backref=db.backref(
            "device_property_calibrations",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    device_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=False
    )
    device_property = db.relationship(
        "DeviceProperty",
        uselist=False,
        foreign_keys=[device_property_id],
        backref=db.backref(
            "device_property_calibrations",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )

    def get_parent(self):
        """Return parent object."""
        return self.device
