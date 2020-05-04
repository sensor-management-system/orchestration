from project.api.models.baseModel import db


class Properties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measuringRangeMin = db.Column(db.Float())
    measuringRangeMax = db.Column(db.Float())
    failureValue = db.Column(db.Float())
    accuracy = db.Column(db.String(30))
    label = db.Column(db.String(30))
    unit = db.Column(db.String(30))
    Compartment = db.Column(db.String(40))
    Variable = db.Column(db.String(50))
    SamplingMedia = db.Column(db.DateTime)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship('Device', backref=db.backref('properties'))
