from project.api.models.base_model import db
from sqlalchemy.sql import func


class Device(db.Model):
    """
    Device class
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    short_name = db.Column(db.String(256))
    long_name = db.Column(db.String(256))
    serial_number = db.Column(db.String(256))
    manufacturer_uri = db.Column(db.String(256))
    manufacturer_name = db.Column(db.String(256))
    dual_use = db.Column(db.Boolean, default=False)
    model = db.Column(db.String(256))
    inventory_number = db.Column(db.String(256))
    persistent_identifier = db.Column(db.String(1024))
    website = db.Column(db.String(1024))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    modified_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    customfields = db.relationship("CustomField",
                                   cascade="save-update, merge, "
                                           "delete, delete-orphan")
