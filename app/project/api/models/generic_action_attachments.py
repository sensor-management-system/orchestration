from ..models.configuration_attachment import ConfigurationAttachment
from .base_model import db


class GenericPlatformActionAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_id = db.Column(
        db.Integer, db.ForeignKey("generic_platform_action.id"), nullable=False
    )
    action = db.relationship(
        "GenericPlatformAction",
        uselist=False,
        foreign_keys=[action_id],
        backref=db.backref("generic_platform_action_attachments"),
    )
    attachment_id = db.Column(
        db.Integer, db.ForeignKey("platform_attachment.id"), nullable=False
    )
    attachment = db.relationship(
        "PlatformAttachment",
        uselist=False,
        foreign_keys=[attachment_id],
        backref=db.backref("generic_platform_action_attachments"),
    )


class GenericDeviceActionAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_id = db.Column(
        db.Integer, db.ForeignKey("generic_device_action.id"), nullable=False
    )
    action = db.relationship(
        "GenericDeviceAction",
        uselist=False,
        foreign_keys=[action_id],
        backref=db.backref("generic_device_action_attachments"),
    )
    attachment_id = db.Column(
        db.Integer, db.ForeignKey("device_attachment.id"), nullable=False
    )
    attachment = db.relationship(
        "DeviceAttachment",
        uselist=False,
        foreign_keys=[attachment_id],
        backref=db.backref("generic_device_action_attachments"),
    )


class GenericConfigurationActionAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_id = db.Column(
        db.Integer, db.ForeignKey("generic_configuration_action.id"), nullable=False
    )
    action = db.relationship(
        "GenericConfigurationAction",
        uselist=False,
        foreign_keys=[action_id],
        backref=db.backref("generic_configuration_action_attachments"),
    )
    attachment_id = db.Column(
        db.Integer, db.ForeignKey("configuration_attachment.id"), nullable=False
    )
    attachment = db.relationship(
        ConfigurationAttachment,
        uselist=False,
        foreign_keys=[attachment_id],
        backref=db.backref("generic_configuration_action_attachments"),
    )
