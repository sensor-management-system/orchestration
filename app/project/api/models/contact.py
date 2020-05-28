from project.api.models.base_model import db


class Contact(db.Model):
    """
    Contact class
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128))
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    email = db.Column(db.String(256), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship('Device', backref=db.backref('contacts'))
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    platform = db.relationship('Platform', backref=db.backref('contacts'))
