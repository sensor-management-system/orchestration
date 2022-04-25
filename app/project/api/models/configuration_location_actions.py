from .base_model import db
from .mixin import AuditMixin, IndirectSearchableMixin


class ConfigurationStaticLocationBeginAction(
    db.Model, AuditMixin, IndirectSearchableMixin
):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref(
            "configuration_static_location_begin_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    begin_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("configuration_static_location_begin_actions"),
    )
    x = db.Column(db.Float, nullable=True)
    y = db.Column(db.Float, nullable=True)
    z = db.Column(db.Float, nullable=True)
    epsg_code = db.Column(db.String(256), default="4326")
    elevation_datum_name = db.Column(db.String(256), default="MSL")  # mean sea level
    elevation_datum_uri = db.Column(db.String(256), nullable=True)

    def get_parent_search_entities(self):
        """Return the configuration as parent search entity."""
        return [self.configuration]

    def to_search_entry(self):
        """Return a dict with search information."""
        return {
            "description": self.description,
        }

    def get_parent(self):
        """Return parent object."""
        return self.configuration


class ConfigurationStaticLocationEndAction(
    db.Model, AuditMixin, IndirectSearchableMixin
):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref(
            "configuration_static_location_end_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("configuration_static_location_end_actions"),
    )

    def get_parent_search_entities(self):
        """Return the configuration as parent search entity."""
        return [self.configuration]

    def to_search_entry(self):
        """Return a dict with search information."""
        return {
            "description": self.description,
        }

    def get_parent(self):
        """Return parent object."""
        return self.configuration


class ConfigurationDynamicLocationBeginAction(
    db.Model, AuditMixin, IndirectSearchableMixin
):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref(
            "configuration_dynamic_location_begin_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    begin_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("configuration_dynamic_location_begin_actions"),
    )
    x_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=True
    )
    x_property = db.relationship(
        "DeviceProperty",
        uselist=False,
        foreign_keys=[x_property_id],
        backref=db.backref("x_property_configuration_dynamic_location_begin_actions"),
    )
    y_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=True
    )
    y_property = db.relationship(
        "DeviceProperty",
        uselist=False,
        foreign_keys=[y_property_id],
        backref=db.backref("y_property_configuration_dynamic_location_begin_actions"),
    )
    z_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=True
    )
    z_property = db.relationship(
        "DeviceProperty",
        uselist=False,
        foreign_keys=[z_property_id],
        backref=db.backref("z_property_configuration_dynamic_location_begin_actions"),
    )
    epsg_code = db.Column(db.String(256), default="4326")
    elevation_datum_name = db.Column(db.String(256), default="MSL")  # mean sea level
    elevation_datum_uri = db.Column(db.String(256), nullable=True)

    def to_search_entry(self):
        """Return a dict with search information."""
        return {
            # We don't include the epsg code or the elevation_datum yet
            "description": self.description,
        }

    def get_parent_search_entities(self):
        """Return the configuration as parent search entity."""
        return [self.configuration]

    def get_parent(self):
        """Return parent object."""
        return self.configuration


class ConfigurationDynamicLocationEndAction(
    db.Model, AuditMixin, IndirectSearchableMixin
):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref(
            "configuration_dynamic_location_end_actions",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("configuration_dynamic_location_end_actions"),
    )

    def to_search_entry(self):
        """Return a dict with search information."""
        return {
            "description": self.description,
        }

    def get_parent_search_entities(self):
        """Return the configuration as parent search entity."""
        return [self.configuration]

    def get_parent(self):
        """Return parent object."""
        return self.configuration
