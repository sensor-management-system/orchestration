from project.api.models.base_model import db


class CustomField(db.Model):
    """
    Custom Field class
    """
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256))
    value = db.Column(db.String(1024))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
