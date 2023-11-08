# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Sqlalchemy model classes for mount actions."""

from ..models.mixin import AuditMixin, IndirectSearchableMixin
from .base_model import db


class PlatformMountAction(db.Model, AuditMixin):
    """Mount of a platform on a configuration."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref(
            "platform_mount_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    platform_id = db.Column(
        db.Integer,
        db.ForeignKey("platform.id"),
        nullable=False,
    )
    platform = db.relationship(
        "Platform",
        uselist=False,
        foreign_keys=[platform_id],
        backref=db.backref("platform_mount_actions"),
    )
    parent_platform_id = db.Column(
        db.Integer, db.ForeignKey("platform.id"), nullable=True
    )
    parent_platform = db.relationship(
        "Platform",
        uselist=False,
        foreign_keys=[parent_platform_id],
        backref=db.backref("outer_platform_mount_actions"),
    )
    begin_date = db.Column(db.DateTime(timezone=True), nullable=False)
    begin_description = db.Column(db.Text, nullable=True)
    begin_contact_id = db.Column(
        db.Integer, db.ForeignKey("contact.id"), nullable=False
    )
    begin_contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[begin_contact_id],
        backref=db.backref("platform_mount_actions"),
    )
    offset_x = db.Column(db.Float, default=0)
    offset_y = db.Column(db.Float, default=0)
    offset_z = db.Column(db.Float, default=0)
    end_date = db.Column(db.DateTime(timezone=True), nullable=True)
    end_description = db.Column(db.Text, nullable=True)
    end_contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=True)
    end_contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[end_contact_id],
        backref=db.backref("platform_unmount_actions"),
    )

    def get_parent_search_entities(self):
        """Return the configuration as parent for the search."""
        # We only want to include the mount for the search in the
        # Configuration.
        return [self.configuration]

    def to_search_entry(self):
        """Return a dict of search slots."""
        return {
            "begin_description": self.begin_description,
            "end_description": self.end_description,
            "platform": self.platform.to_search_entry(),
        }

    def get_parent(self):
        """Return parent object."""
        return self.platform


class DeviceMountAction(db.Model, AuditMixin, IndirectSearchableMixin):
    """Mount of a device on a configuration."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref(
            "device_mount_actions", cascade="save-update, merge, delete, delete-orphan"
        ),
    )
    device_id = db.Column(
        db.Integer,
        db.ForeignKey("device.id"),
        nullable=False,
    )
    device = db.relationship(
        "Device",
        uselist=False,
        foreign_keys=[device_id],
        backref=db.backref("device_mount_actions"),
    )
    parent_platform_id = db.Column(
        db.Integer,
        db.ForeignKey("platform.id"),
        nullable=True,
    )
    parent_platform = db.relationship(
        "Platform",
        uselist=False,
        foreign_keys=[parent_platform_id],
        backref=db.backref(
            "outer_device_mount_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    parent_device_id = db.Column(
        db.Integer,
        db.ForeignKey("device.id"),
        nullable=True,
    )
    parent_device = db.relationship(
        "Device",
        uselist=False,
        foreign_keys=[parent_device_id],
        backref=db.backref(
            "outer_device_mount_actions_for_devices",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    begin_date = db.Column(db.DateTime(timezone=True), nullable=False)
    begin_description = db.Column(db.Text, nullable=True)
    begin_contact_id = db.Column(
        db.Integer, db.ForeignKey("contact.id"), nullable=False
    )
    begin_contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[begin_contact_id],
        backref=db.backref("device_mount_actions"),
    )
    offset_x = db.Column(db.Float, default=0)
    offset_y = db.Column(db.Float, default=0)
    offset_z = db.Column(db.Float, default=0)

    end_date = db.Column(db.DateTime(timezone=True), nullable=True)
    end_description = db.Column(db.Text, nullable=True)
    end_contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=True)
    end_contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[end_contact_id],
        backref=db.backref("device_unmount_actions"),
    )

    def get_parent_search_entities(self):
        """Return the configuration as parent for the search."""
        # We only want to include the mount for the search in the
        # Configuration.
        return [self.configuration]

    def to_search_entry(self):
        """Return a dict of search slots."""
        return {
            "begin_description": self.begin_description,
            "end_description": self.end_description,
            "device": self.device.to_search_entry(),
        }

    def get_parent(self):
        """Return parent object."""
        return self.device
