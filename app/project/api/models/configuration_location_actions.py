from safrs import SAFRSBase

from project.api.models.base_model import db
from project.api.models.mixin import AuditMixin


class ConfigurationStaticLocationBeginAction(db.Model, AuditMixin, SAFRSBase):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref("configuration_static_location_begin_action"),
    )
    begin_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("configuration_static_location_begin_action"),
    )
    x = db.Column(db.Float, nullable=True)
    y = db.Column(db.Float, nullable=True)
    z = db.Column(db.Float, nullable=True)
    epsg_code = db.Column(db.String(256), default="4326")
    elevation_datum_name = db.Column(db.String(256), default="MSL")  # mean sea level
    elevation_datum_uri = db.Column(db.String(256), nullable=True)


class ConfigurationStaticLocationEndAction(db.Model, AuditMixin, SAFRSBase):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref("configuration_static_location_end_action"),
    )
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("configuration_static_location_end_action"),
    )


class ConfigurationDynamicLocationBeginAction(db.Model, AuditMixin, SAFRSBase):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref("configuration_dynamic_location_begin_action"),
    )
    begin_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("configuration_dynamic_location_begin_action"),
    )
    x_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=True
    )
    x_property = db.relationship(
        "DeviceProperty",
        uselist=False,
        foreign_keys=[x_property_id],
        backref=db.backref("configuration_dynamic_location_begin_action_x_property"),
    )
    y_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=True
    )
    y_property = db.relationship(
        "DeviceProperty",
        uselist=False,
        foreign_keys=[y_property_id],
        backref=db.backref("configuration_dynamic_location_begin_action_y_property"),
    )
    z_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=True
    )
    z_property = db.relationship(
        "DeviceProperty",
        uselist=False,
        foreign_keys=[z_property_id],
        backref=db.backref("configuration_dynamic_location_begin_action_z_property"),
    )
    epsg_code = db.Column(db.String(256), default="4326")
    elevation_datum_name = db.Column(db.String(256), default="MSL")  # mean sea level
    elevation_datum_uri = db.Column(db.String(256), nullable=True)


class ConfigurationDynamicLocationEndAction(db.Model, AuditMixin, SAFRSBase):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        uselist=False,
        foreign_keys=[configuration_id],
        backref=db.backref("configuration_dynamic_location_end_action"),
    )
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship(
        "Contact",
        uselist=False,
        foreign_keys=[contact_id],
        backref=db.backref("configuration_dynamic_location_end_action"),
    )
