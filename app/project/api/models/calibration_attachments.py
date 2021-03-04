from project.api.models.base_model import db


class DeviceCalibrationAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_id = db.Column(
        db.Integer, db.ForeignKey("device_calibration_action.id"), nullable=False
    )
    action = db.relationship(
        "DeviceCalibrationAction",
        uselist=False,
        foreign_keys=[action_id],
        backref=db.backref("device_calibration_attachments"),
    )
    attachment_id = db.Column(
        db.Integer, db.ForeignKey("device_attachment.id"), nullable=False
    )
    attachment = db.relationship(
        "DeviceAttachment",
        uselist=False,
        foreign_keys=[attachment_id],
        backref=db.backref("device_calibration_attachments"),
    )
