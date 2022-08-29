"""Model for the users."""

import binascii
import os

from .base_model import db


class User(db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(256), nullable=False, unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    # uselist: To convert one-to-many into one-to-one
    contact = db.relationship("Contact", backref=db.backref("user", uselist=False))
    active = db.Column(db.Boolean, default=True)
    is_superuser = db.Column(db.Boolean, default=False)
    apikey = db.Column(db.String(256), unique=True)

    @staticmethod
    def generate_new_apikey():
        """
        Generate a new api key.

        This method doesn't set the value in the model.
        It just generates a new key.
        """
        return binascii.b2a_hex(os.urandom(64)).decode("ascii")

    def __str__(self):
        """Return a string representation of the user."""
        return f"User(subject={repr(self.subject)})"
