from ..models.mixin import AuditMixin, IndirectSearchableMixin
from .base_model import db


class GenericPlatformAction(db.Model, AuditMixin, IndirectSearchableMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    platform = db.relationship(
        "Platform",
        uselist=False,
        foreign_keys=[platform_id],
        backref=db.backref(
            "generic_platform_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    description = db.Column(db.Text, nullable=True)
    action_type_name = db.Column(db.String(256), nullable=False)
    action_type_uri = db.Column(db.String(256), nullable=True)
    begin_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("generic_platform_actions"),
    )

    def get_parent_search_entities(self):
        """Return the platform as parent."""
        # We won't search for the contact of this action, so we skip it here.
        return [self.platform]

    def to_search_entry(self):
        """Return a dict with the search fields."""
        return {
            "action_type_name": self.action_type_name,
            "action_type_uri": self.action_type_uri,
            "description": self.description,
        }


class GenericDeviceAction(db.Model, AuditMixin, IndirectSearchableMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(
        "Device",
        uselist=False,
        foreign_keys=[device_id],
        backref=db.backref(
            "generic_device_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    description = db.Column(db.Text, nullable=True)
    action_type_name = db.Column(db.String(256), nullable=False)
    action_type_uri = db.Column(db.String(256), nullable=True)
    begin_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref(
            "generic_device_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )

    def get_parent_search_entities(self):
        """Return the device as parent."""
        # We won't search for the contact of this action, so we skip it here.
        return [self.device]

    def to_search_entry(self):
        """Return a dict with the search fields."""
        return {
            "action_type_name": self.action_type_name,
            "action_type_uri": self.action_type_uri,
            "description": self.description,
        }


class GenericConfigurationAction(db.Model, AuditMixin, IndirectSearchableMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref(
            "generic_configuration_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    description = db.Column(db.Text, nullable=True)
    action_type_name = db.Column(db.String(256), nullable=False)
    action_type_uri = db.Column(db.String(256), nullable=True)
    begin_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("generic_configuration_actions"),
    )

    def get_parent_search_entities(self):
        """Return the configuration as parent."""
        # We won't search for the contact of this action, so we skip it here.
        return [self.configuration]

    def to_search_entry(self):
        """Return a dict with the search fields."""
        return {
            "action_type_name": self.action_type_name,
            "action_type_uri": self.action_type_uri,
            "description": self.description,
        }
