

from project.api.models.base_model import db


class DeviceSoftwareUpdateActionAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_id = db.Column(
        db.Integer, db.ForeignKey("device_software_update_action.id"), nullable=False
    )
    action = db.relationship(
        "DeviceSoftwareUpdateAction",
        uselist=False,
        foreign_keys=[action_id],
        backref=db.backref("device_software_update_action_attachments"),
    )
    attachment_id = db.Column(
        db.Integer, db.ForeignKey("device_attachment.id"), nullable=False
    )
    attachment = db.relationship(
        "DeviceAttachment",
        uselist=False,
        foreign_keys=[attachment_id],
        backref=db.backref("device_software_update_action_attachments"),
    )


class PlatformSoftwareUpdateActionAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_id = db.Column(
        db.Integer, db.ForeignKey("platform_software_update_action.id"), nullable=False
    )
    action = db.relationship(
        "PlatformSoftwareUpdateAction",
        uselist=False,
        foreign_keys=[action_id],
        backref=db.backref("platform_software_update_action_attachments"),
    )
    attachment_id = db.Column(
        db.Integer, db.ForeignKey("platform_attachment.id"), nullable=False
    )
    attachment = db.relationship(
        "PlatformAttachment",
        uselist=False,
        foreign_keys=[attachment_id],
        backref=db.backref("platform_software_update_action_attachments"),
    )
