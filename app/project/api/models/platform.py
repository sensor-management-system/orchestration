from project.api.models.baseModel import db


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(400))
    shortName = db.Column(db.String(10))
    longName = db.Column(db.String(128))
    manufacturer = db.Column(db.String(128))
    type = db.Column(db.String(128))
    platformType = db.Column(db.String(128))
    urn = db.Column(db.String(256))
    src = db.Column(db.String(400))
    configurationDate = db.Column(db.DateTime)
    inventoryNumber = db.Column(db.String)
