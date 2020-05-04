from project.api.models.baseModel import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    Date = db.Column(db.DateTime)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship('Device', backref=db.backref('events'))
