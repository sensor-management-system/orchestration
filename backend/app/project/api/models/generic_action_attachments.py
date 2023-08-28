# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from .base_model import db
from ..models.configuration_attachment import ConfigurationAttachment


class GenericPlatformActionAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_id = db.Column(
        db.Integer, db.ForeignKey("generic_platform_action.id"), nullable=False
    )
    action = db.relationship(
        "GenericPlatformAction",
        uselist=False,
        foreign_keys=[action_id],
        backref=db.backref(
            "generic_platform_action_attachments",
            cascade="save-update, merge, delete, delete-orphan",
        ),
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

    def get_parent(self):
        """Return parent object."""
        return self.attachment.platform


class GenericDeviceActionAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_id = db.Column(
        db.Integer, db.ForeignKey("generic_device_action.id"), nullable=False
    )
    action = db.relationship(
        "GenericDeviceAction",
        uselist=False,
        foreign_keys=[action_id],
        backref=db.backref(
            "generic_device_action_attachments",
            cascade="save-update, merge, delete, delete-orphan",
        ),
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

    def get_parent(self):
        """Return parent object."""
        return self.attachment.device


class GenericConfigurationActionAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_id = db.Column(
        db.Integer, db.ForeignKey("generic_configuration_action.id"), nullable=False
    )
    action = db.relationship(
        "GenericConfigurationAction",
        uselist=False,
        foreign_keys=[action_id],
        backref=db.backref(
            "generic_configuration_action_attachments",
            cascade="save-update, merge, delete, delete-orphan",
        ),
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

    def get_parent(self):
        """Return parent object."""
        return self.attachment.configuration
