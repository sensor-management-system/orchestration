# SPDX-FileCopyrightText: 2021
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from .base_model import db


class DeviceSoftwareUpdateActionAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_id = db.Column(
        db.Integer, db.ForeignKey("device_software_update_action.id"), nullable=False
    )
    action = db.relationship(
        "DeviceSoftwareUpdateAction",
        uselist=False,
        foreign_keys=[action_id],
        backref=db.backref(
            "device_software_update_action_attachments",
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
        backref=db.backref(
            "platform_software_update_action_attachments",
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
        backref=db.backref("platform_software_update_action_attachments"),
    )
