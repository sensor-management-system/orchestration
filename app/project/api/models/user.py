from project.api.models.base_model import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(256))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship('Contact', backref=db.backref('user'))

    def __str__(self):
        return "User(id='%s')" % self.id
