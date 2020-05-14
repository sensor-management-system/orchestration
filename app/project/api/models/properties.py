from project.api.models.baseModel import db


class Properties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measuring_range_min = db.Column(db.Float())
    measuring_range_max = db.Column(db.Float())
    failure_value = db.Column(db.Float())
    accuracy = db.Column(db.String(30))
    label = db.Column(db.String(30))
    unit = db.Column(db.String(30))  # vermutlich CV
    Compartment = db.Column(db.String(40))  # vermutlich CV
    Variable = db.Column(db.String(50))  # vermutlich CV
    # vermutlich CV, z.B. Atmosphere, Pedosphere
    sampling_media = db.Column(db.String(256))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship('Device', backref=db.backref('properties'))
