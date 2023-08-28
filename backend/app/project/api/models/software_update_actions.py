# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from ..models.mixin import AuditMixin, IndirectSearchableMixin
from .base_model import db


class DeviceSoftwareUpdateAction(db.Model, AuditMixin, IndirectSearchableMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(
        "Device",
        uselist=False,
        foreign_keys=[device_id],
        backref=db.backref(
            "device_software_update_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    software_type_name = db.Column(db.String(256), nullable=False)
    software_type_uri = db.Column(db.String(256), nullable=True)
    update_date = db.Column(db.DateTime(timezone=True), nullable=False)
    version = db.Column(db.String(256), nullable=True)
    repository_url = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("device_software_update_actions"),
    )

    def get_parent_search_entities(self):
        """Return the device as parent."""
        return [self.device]

    def to_search_entry(self):
        """Return a dict with search information."""
        return {
            "software_type_name": self.software_type_name,
            "software_type_uri": self.software_type_uri,
            "version": self.version,
            "repository_url": self.repository_url,
            "description": self.description,
        }

    def get_parent(self):
        """Return parent object."""
        return self.device


class PlatformSoftwareUpdateAction(db.Model, AuditMixin, IndirectSearchableMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    platform = db.relationship(
        "Platform",
        uselist=False,
        foreign_keys=[platform_id],
        backref=db.backref(
            "platform_software_update_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    software_type_name = db.Column(db.String(256), nullable=False)
    software_type_uri = db.Column(db.String(256), nullable=True)
    update_date = db.Column(db.DateTime(timezone=True), nullable=False)
    version = db.Column(db.String(256), nullable=True)
    repository_url = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("platform_software_update_actions"),
    )

    def get_parent_search_entities(self):
        """Return the platform as parent."""
        return [self.platform]

    def to_search_entry(self):
        """Return a dict with search information."""
        return {
            "software_type_name": self.software_type_name,
            "software_type_uri": self.software_type_uri,
            "version": self.version,
            "repository_url": self.repository_url,
            "description": self.description,
        }

    def get_parent(self):
        """Return parent object."""
        return self.platform
