# SPDX-FileCopyrightText: 2020 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

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
    contact = db.relationship(
        "Contact", backref=db.backref("user", uselist=False), foreign_keys=[contact_id]
    )
    active = db.Column(db.Boolean, default=True)
    is_superuser = db.Column(db.Boolean, default=False)
    is_export_control = db.Column(db.Boolean, default=False)
    apikey = db.Column(db.String(256), unique=True)
    terms_of_use_agreement_date = db.Column(db.DateTime(timezone=True), nullable=True)

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
