from project.api.models.base_model import db


class Platform(db.Model):
    """
    Platform class
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    short_name = db.Column(db.String(256))
    long_name = db.Column(db.String(256))
    manufacturer = db.Column(db.String(256))
    type = db.Column(db.String(256))
    platform_type = db.Column(db.String(256))
    url = db.Column(db.String(1024))
    configuration_date = db.Column(db.DateTime)
    inventory_number = db.Column(db.String(256))
