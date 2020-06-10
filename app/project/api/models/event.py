from project.api.models.base_model import db


class Event(db.Model):
    """
    Event class
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('events'))
