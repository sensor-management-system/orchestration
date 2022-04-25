from .base_model import db
from ..models.mixin import AuditMixin, IndirectSearchableMixin


class PlatformUnmountAction(db.Model, AuditMixin, IndirectSearchableMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref(
            "platform_unmount_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    platform = db.relationship(
        "Platform",
        uselist=False,
        foreign_keys=[platform_id],
        backref=db.backref("platform_unmount_actions"),
    )
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
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
            "description": self.description,
        }

    def get_parent(self):
        """Return parent object."""
        return self.platform


class DeviceUnmountAction(db.Model, AuditMixin, IndirectSearchableMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref(
            "device_unmount_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(
        "Device",
        uselist=False,
        foreign_keys=[device_id],
        backref=db.backref("device_unmount_actions"),
    )
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
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
            "description": self.description,
        }

    def get_parent(self):
        """Return parent object."""
        return self.device
