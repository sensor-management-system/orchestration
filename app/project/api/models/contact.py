from project.api.models.base_model import db

platform_contacts = db.Table('platform_contacts',
                             db.Column('platform_id', db.Integer,
                                       db.ForeignKey('platform.id'),
                                       primary_key=True),
                             db.Column('contact_id', db.Integer,
                                       db.ForeignKey('contact.id'),
                                       primary_key=True)
                             )

device_contacts = db.Table('device_contacts',
                           db.Column('device_id', db.Integer,
                                     db.ForeignKey('device.id'),
                                     primary_key=True),
                           db.Column('contact_id', db.Integer,
                                     db.ForeignKey('contact.id'),
                                     primary_key=True)
                           )


class Contact(db.Model):
    """
    Contact class
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    given_name = db.Column(db.String(256))
    family_name = db.Column(db.String(256))
    website = db.Column(db.String(1024))
    email = db.Column(db.String(256), nullable=False)
    devices = db.relationship('Device', secondary=device_contacts, lazy='subquery',
                              backref=db.backref('contacts', lazy=True))
    platforms = db.relationship('Platform', secondary=platform_contacts, lazy='subquery',
                                backref=db.backref('contacts', lazy=True))
