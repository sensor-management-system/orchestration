# SPDX-FileCopyrightText: 2025
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Classes for the permission group membership."""

from .base_model import db

class PermissionGroupMembership(db.Model):
    """Model for the membership of a user in a group."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_group_id = db.Column(
        db.Integer, db.ForeignKey("permission_group.id"), nullable=False
    )
    permission_group = db.relationship(
        "PermissionGroup",
        backref=db.backref(
            "memberships",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    user = db.relationship(
        "User",
        backref=db.backref(
            "memberships",
            cascade="save-update, merge, delete, delete-orphan",
        ),
    )
