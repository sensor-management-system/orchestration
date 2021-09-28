from .base_model import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(256), nullable=False, unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    # uselist: To convert one-to-many into one-to-one
    contact = db.relationship("Contact", backref=db.backref("user", uselist=False))
    active = db.Column(db.Boolean, default=True)

    def __str__(self):
        return "User(username='%s')" % self.subject.split("@")[0]
