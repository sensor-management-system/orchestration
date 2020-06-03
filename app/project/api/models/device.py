from project.api.models.base_model import db


class Device(db.Model):
    """
    Device class
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    short_name = db.Column(db.String(256))
    long_name = db.Column(db.String(256))
    serial_number = db.Column(db.String(256))
    manufacturer = db.Column(db.String(256))
    dual_use = db.Column(db.Boolean, default=False)
    model = db.Column(db.String(256))
    inventory_number = db.Column(db.String(256))
    persistent_identifier = db.Column(db.String(1024))
    url = db.Column(db.String(1024))
    label = db.Column(db.String(256))
    type = db.Column(db.String(256))
    configuration_date = db.Column(db.DateTime)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    platform = db.relationship('Platform', backref=db.backref('devices'))
