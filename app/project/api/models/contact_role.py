from .base_model import db

contact_roles = db.Table(
    "contact_role",
    db.Column("contact_id", db.Integer, db.ForeignKey("contact.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
)


class Role(db.Model):
    """Contact Role"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    uri = db.Column(db.String(256), nullable=False)
    contacts = db.relationship(
        "Contact",
        secondary=contact_roles,
        lazy="subquery",
        backref=db.backref("roles", lazy=True),
    )

    def __repr__(self):
        return "<Role %r>" % self.name
