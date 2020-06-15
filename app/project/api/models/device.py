from project.api.models.base_model import db
from project.api.models.mixin import AuditMixin


class Device(db.Model, AuditMixin):
    """
    Device class
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=True)
    short_name = db.Column(db.String(256), nullable=False)
    long_name = db.Column(db.String(256), nullable=True)
    serial_number = db.Column(db.String(256), nullable=True)
    manufacturer_uri = db.Column(db.String(256), nullable=True)
    manufacturer_name = db.Column(db.String(256), nullable=True)
    dual_use = db.Column(db.Boolean, default=False)
    model = db.Column(db.String(256), nullable=True)
    inventory_number = db.Column(db.String(256), nullable=True)
    persistent_identifier = db.Column(db.String(256), nullable=True,
                                      unique=True)
    website = db.Column(db.String(1024), nullable=True)
    customfields = db.relationship("CustomField",
                                   cascade="save-update, merge, "
                                           "delete, delete-orphan")
    device_properties = db.relationship("DeviceProperty",
                                        cascade="save-update, merge, "
                                                "delete, delete-orphan")
    events = db.relationship("Event",
                             cascade="save-update, merge, "
                                     "delete, delete-orphan")

    device_attachments = db.relationship("DeviceAttachment",
                                         cascade="save-update, merge, "
                                                 "delete, delete-orphan")
