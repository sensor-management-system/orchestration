from project.api.models.base_model import db


class Attachment(db.Model):
    """
    Attachment class
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(256))
    url = db.Column(db.String(1024), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship('Device', backref=db.backref('attachment'))
