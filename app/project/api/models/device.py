from project.api.models.baseModel import db


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    shortName = db.Column(db.String(30))
    longName = db.Column(db.String(128))
    serialNumber = db.Column(db.Integer)
    manufacture = db.Column(db.String(128))
    dualUse = db.Column(db.Boolean, default=False)
    model = db.Column(db.String(128))
    inventoryNumber = db.Column(db.Integer)
    persistentIdentifier = db.Column(db.String(128))
    website = db.Column(db.String(200))
    label = db.Column(db.String(128))
    type = db.Column(db.String(128))
    #deviceURN = db.Column(db.String(300))
    configurationDate = db.Column(db.DateTime)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    platform = db.relationship('Platform', backref=db.backref('devices'))
