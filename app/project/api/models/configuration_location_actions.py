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
    begin_description = db.Column(db.Text, nullable=True)
    begin_contact_id = db.Column(
        db.Integer, db.ForeignKey("contact.id"), nullable=False
    )
    begin_contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[begin_contact_id],
        backref=db.backref("configuration_static_location_begin_actions"),
    )
    x = db.Column(db.Float, nullable=True)
    y = db.Column(db.Float, nullable=True)
    z = db.Column(db.Float, nullable=True)
    epsg_code = db.Column(db.String(256), default="4326")
    elevation_datum_name = db.Column(db.String(256), default="MSL")  # mean sea level
    elevation_datum_uri = db.Column(db.String(256), nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    end_description = db.Column(db.Text, nullable=True)
    end_contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=True)
    end_contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[end_contact_id],
        backref=db.backref("configuration_static_location_end_actions"),
    )

    def get_parent_search_entities(self):
        """Return the configuration as parent search entity."""
        return [self.configuration]

    def to_search_entry(self):
        """Return a dict with search information."""
        return {
            "begin_description": self.begin_description,
            "end_description": self.end_description,
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
    begin_description = db.Column(db.Text, nullable=True)
    begin_contact_id = db.Column(
        db.Integer, db.ForeignKey("contact.id"), nullable=False
    )
    begin_contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[begin_contact_id],
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
    end_date = db.Column(db.DateTime, nullable=True)
    end_description = db.Column(db.Text, nullable=True)
    end_contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=True)
    end_contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[end_contact_id],
        backref=db.backref("configuration_dynamic_location_end_actions"),
    )

    def to_search_entry(self):
        """Return a dict with search information."""
        return {
            # We don't include the epsg code or the elevation_datum yet
            "begin_description": self.begin_description,
            "end_description": self.end_description,
        }

    def get_parent_search_entities(self):
        """Return the configuration as parent search entity."""
        return [self.configuration]

    def get_parent(self):
        """Return parent object."""
        return self.configuration
